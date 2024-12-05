import numpy as np
from scipy.io import wavfile

# Parameters
frequency = 150  # Frequency in Hz. Adjust as needed for optimal cancellation
sample_rate = 44100  # Standard sample rate for high-quality audio
duration = 10.0  # Duration of the tone in seconds
fade_duration = 0.1  # Duration of fade-in and fade-out in seconds

# Explanation:
# Lower frequencies are less affected by slight timing differences between devices,
# making cancellation more noticeable despite synchronization challenges.

# Generate a time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
# 'endpoint=False' ensures the endpoint is not included, matching the desired number of samples

# Generate the tone (sine wave)
tone = np.sin(2 * np.pi * frequency * t)

# Generate the inverse tone by inverting the phase (180 degrees out of phase)
inverse_tone = -tone  # Equivalent to np.sin(2 * np.pi * frequency * t + np.pi)

# Normalize the amplitude to prevent distortion during playback
max_amplitude = np.iinfo(np.int16).max  # Maximum value for 16-bit audio
tone = tone / np.max(np.abs(tone)) * max_amplitude  # Scale to 16-bit range
inverse_tone = inverse_tone / np.max(np.abs(inverse_tone)) * max_amplitude

# Apply fade-in and fade-out to eliminate clicking sounds at the start and end
fade_samples = int(fade_duration * sample_rate)  # Number of samples over which to apply fade
fade_in = np.linspace(0, 1, fade_samples)  # Fade-in multiplier from 0 to 1
fade_out = np.linspace(1, 0, fade_samples)  # Fade-out multiplier from 1 to 0

# Apply fade-in to the beginning of the tones
tone[:fade_samples] *= fade_in
inverse_tone[:fade_samples] *= fade_in

# Apply fade-out to the end of the tones
tone[-fade_samples:] *= fade_out
inverse_tone[-fade_samples:] *= fade_out

# Convert the numpy arrays to 16-bit integers for WAV file format
tone = tone.astype(np.int16)
inverse_tone = inverse_tone.astype(np.int16)

# Save the tones as high-quality WAV files
wavfile.write('tone.wav', sample_rate, tone)
wavfile.write('inverse_tone.wav', sample_rate, inverse_tone)
