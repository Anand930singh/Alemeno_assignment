import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

@csrf_exempt
def urineStripAnalyzer(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
        file_path = default_storage.path(file_name)
        logger = logging.getLogger(__name__)

        logger.info(f"Image saved at: {file_path}")

        # Load the image in grayscale
        image = cv2.imread(file_path)
        image_gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Apply bilateral filter
        bilateral_filtered = cv2.bilateralFilter(image_gray, 9, 75, 75)

        # Apply adaptive thresholding
        binary_adaptive = cv2.adaptiveThreshold(bilateral_filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Create a structuring element (kernel)
        kernel = np.ones((5, 5), np.uint8)

        # Complement the binary image
        complemented_image = cv2.bitwise_not(binary_adaptive)

        # Apply dilation
        dilated_image = cv2.dilate(complemented_image, kernel, iterations=2)

        # Apply erosion
        eroded_image = cv2.erode(dilated_image, kernel, iterations=2)

        # Complement the eroded image
        again_complement = cv2.bitwise_not(eroded_image)

        contour_labels = {
            'URO': None,
            'BIL': None,
            'KET': None,
            'BLD': None,
            'PRO': None,
            'NIT': None,
            'LEU': None,
            'GLU': None,
            'SG': None,
            'PH': None
        }
        rgb_positions=[]
        (cnts, h) = cv2.findContours(again_complement.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        filtered_contours = []
        for contour in cnts:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            if len(approx) >= 4 and len(approx) <= 8 and 3000 < cv2.contourArea(contour) < 8000:
                cv2.drawContours(image_gray, [contour], -1, (0, 255, 0), 5)

                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    cX, cY = 0, 0

                rgb_value = image[cY, cX]
                b, g, r = rgb_value
                filtered_contours.append([int(r), int(g), int(b)])  # Convert to native int
                rgb_positions.append({
                    'rgb': [int(r), int(g), int(b)],  # Convert to native int
                    'coordinates': (cX, cY)
                })

        reversed_list = filtered_contours[::-1]

        for label, rgb_values in zip(contour_labels.keys(), reversed_list):
            contour_labels[label] = rgb_values

        # default_storage.delete(file_name)

        return JsonResponse({
            'contour_labels': contour_labels,
            'rgb_positions': rgb_positions
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
