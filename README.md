# Vocal Tract Tube Model

Given a recording of a human saying "aah", this project: 

1. Simulates a series of tubes that can be used to generate a sound, in accordance with
   the N-tube model of human speech production. 
2. Optimizes over the dimensions of these tubes, returning the model that best mimics
   human speech (over a variety of loss functions, we used a modified DTW loss over the 
   Fourier transform of the target + model sounds). 
3. Generates `.wav` files containing the model's output sounds. 

## Attributions. 

Based off [Shun60s' original model](https://github.com/shun60s/Vocal-Tube-Model).
We've generalized his model to N tubes, added in an optimizer framework, and made 
some other changes. 

## Project Group

- Arman Durrani
- Jacob Levine
- Justine Lin
- Ravit Sharma
- Sasha Kononova
- Yash Lala

## License

MIT License, copyright held by [Shun60s](https://github.com/shun60s).
