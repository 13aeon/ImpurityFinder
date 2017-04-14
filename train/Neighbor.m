function Nei = Neighbor(i, j, m, n)
Nei = [i - 1 + (j-1)*m, i + 1 + (j-1)*m, i + (j-2)*m, i + j*m];
Mask = [];
if i == 1
    Mask = [Mask 1];
end
if i == m
    Mask = [Mask 2];
end
if j == 1
    Mask = [Mask 3];
end
if j == n
    Mask = [Mask 4];
end
Nei(Mask) = [];

