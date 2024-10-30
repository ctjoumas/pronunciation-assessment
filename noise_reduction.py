# noise_reduction.py

import noisereduce as nr
from scipy.io import wavfile
from io import BytesIO

def reduce_background_noise(input_file, noise_sample_duration=10):
    """
    Reduce background noise in an audio file.

    Parameters:
    - input_file: A file-like object containing the WAV audio data.
    - noise_sample_duration: Duration (in seconds) to use as the noise sample from the beginning.

    """
    # Read WAV file data and sample rate
    rate, data = wavfile.read(input_file)

    # Define the noise sample
    noise_sample = data[:int(rate * noise_sample_duration)]
    
    # Apply noise reduction with supported parameters
    reduced_noise = nr.reduce_noise(
        y=data,
        sr=rate,
        y_noise=noise_sample,
        prop_decrease=0.95  # Only use prop_decrease if supported
    )
    
    # Save the processed audio to an in-memory file
    output_file = BytesIO()
    wavfile.write(output_file, rate, reduced_noise.astype(data.dtype))  # Ensure matching data type
    output_file.seek(0)  # Reset buffer to the beginning for reading
    return output_file
# End of noise_reduction.py