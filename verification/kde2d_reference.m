% Add reference implementation to search path.
addpath('kde');

% Generate 1000 data points from a 2d normal distribution.
rng(1);
N = 1000;
x = randn(N, 1);
y = randn(N, 1);

% Estimate the 2d density within +/- 5 standard deviations.
l = 5;
n = 256;
[~, density, ~, ~] = kde2d([x, y], n, [-l -l], [+l +l]);
