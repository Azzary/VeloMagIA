let session;

async function loadModel() {
    try {
        session = await ort.InferenceSession.create('/static/bike_predictor.onnx');
        console.log('Model loaded successfully');
    } catch (e) {
        console.error('Failed to load model:', e);
    }
}

async function predict(inputs) {
    try {
        const inputTensor = new ort.Tensor('float32', inputs, [1, 18]);
        const outputMap = await session.run({ 'input': inputTensor });
        return outputMap['output'].data[0];
    } catch (e) {
        console.error('Prediction failed:', e);
        return null;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadModel();

    const form = document.getElementById('predictForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const inputs = [
            // Assurez-vous que l'ordre correspond à celui de votre modèle
            formData.get('is_weekend') === 'on' ? 1 : 0,
            formData.get('is_holiday') === 'on' ? 1 : 0,
            formData.get('is_school_vacation') === 'on' ? 1 : 0,
            parseInt(formData.get('day_of_week')),
            parseFloat(formData.get('temp')),
            parseFloat(formData.get('max_temp')),
            parseFloat(formData.get('min_temp')),
            parseFloat(formData.get('precipitation')),
            parseFloat(formData.get('wind_speed')),
            parseFloat(formData.get('visibility')),
            formData.get('fog') === 'on' ? 1 : 0,
            formData.get('rain') === 'on' ? 1 : 0,
            formData.get('snow') === 'on' ? 1 : 0,
            formData.get('hail') === 'on' ? 1 : 0,
            formData.get('thunder') === 'on' ? 1 : 0,
            formData.get('tornado') === 'on' ? 1 : 0,
            parseInt(formData.get('hour')),
            parseInt(formData.get('minute'))
        ];

        const prediction = await predict(inputs);
        const resultElement = document.getElementById("result");
        if (prediction !== null) {
            resultElement.textContent = `Predicted number of bikes: ${prediction.toFixed(2)}`;
            resultElement.classList.add('visible');
        } else {
            resultElement.textContent = 'Prediction failed';
            resultElement.classList.add('visible');
        }
    });
});