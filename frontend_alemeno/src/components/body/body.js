import React, { useState } from 'react';
import './body.css';
import Download from '../../assets/download.png';
import { JsonView, allExpanded, darkStyles} from 'react-json-view-lite';
import "react-json-view-lite/dist/index.css";

function Body() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [responseData, setResponseData] = useState(null);

  // Function to handle file selection
  const handleImageUpload = (e) => {
    const file = e.target.files[0]; // Assuming single file selection
    setSelectedImage(file);
  };

  // Function to handle form submission
  const handleSubmit = async () => {
    if (!selectedImage) {
      alert("Please select an image first!");
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedImage);
    console.log('hii')
    try {
      const response = await fetch('http://127.0.0.1:8000/api/urineStrip/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResponseData(data);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className='container'>
    <div className='bodyContain'>
      <div className='leftBody'>
        <label htmlFor="uploadInput">
          <img className='uploadIcon' src={Download} alt="Upload Image" width='80' height='80' />
        </label>
        <input
          id="uploadInput"
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleImageUpload}
        />
        <div className='tagline'>Upload Your Urine Strip Image</div>
        {selectedImage && (
          <div className="selectedImageName">{selectedImage.name}</div>
        )}
        <button className='button-3' onClick={handleSubmit}>Submit</button>
      </div>
      <div className='rightBody'>
          <div className='imgContain'>
            {selectedImage ? (
              <img src={URL.createObjectURL(selectedImage)} alt="Selected" />
            ) : (
              <div className="selectImageText">Select Image for Report</div>
            )}
            {responseData && responseData.rgb_positions && responseData.rgb_positions.map((position, index) => (
              <div
                key={index}
                className="rgbText"
                style={{
                  top: `${position.coordinates[1]/3.6}px`,
                  left: `${position.coordinates[0]/2.1}px`,
                }}
              >
                {`RGB: (${position.rgb.join(', ')})`}
              </div>
            ))}
          </div>
      </div>
    </div>
    <div className='jsonViewer'>
    {responseData && responseData.contour_labels && (
        <JsonView data={responseData.contour_labels} shouldExpandNode={allExpanded} style={darkStyles} />
    )}
    </div>
    </div>
  );
}

export default Body;
