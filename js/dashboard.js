document.addEventListener('DOMContentLoaded', () => {
    const videoInput = document.getElementById('videoFile');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const previewImage = document.getElementById('previewImage');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');

    videoInput.addEventListener('change', () => {
        if (videoInput.files.length > 0) {
            analyzeBtn.style.display = 'inline-block';
        } else {
            analyzeBtn.style.display = 'none';
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const file = videoInput.files[0];
        if (!file) {
            alert('Please select a video file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            loading.style.display = 'block';
            result.textContent = '';
            previewImage.style.display = 'none';

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                // Display the extracted frame
                previewImage.src = data.frame_url;
                previewImage.style.display = 'block';

                // Show the result
                result.textContent = `Prediction: ${data.prediction} (Confidence: ${data.confidence})`;
                result.style.color = data.color;
            } else {
                alert(data.error || 'Analysis failed');
            }
        } catch (error) {
            alert('Error during analysis');
        } finally {
            loading.style.display = 'none';
        }
    });
});