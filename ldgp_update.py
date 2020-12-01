import numpy as np


class Calculator:
    def __init__(self, num_points, R, block_size):
        self.num_points = num_points
        self.R = R
        self.block_size = block_size
        self.counter = 0

    def encod(self, a, b):
        value = 0
        if a > b:
            value = 1
        return value

    def distribute_val(self, val, a, b):
        ratio = (val - a) / (b - a)
        val_a = round(val * ratio)
        val_b = val - val_a
        return val_a, val_b

    def block_hist(self, data):
        bins = [0, 8, 16, 24, 32, 40, 48, 56, 64]
        hist_bin = {'0': 0, '8': 0, '16': 0, '24': 0, '32': 0, '40': 0, '48': 0, '56': 0, '64': 0}
        for v in data:
            for b in range(8):
                if v >= bins[b] & v < bins[b + 1]:
                    p, q = self.distribute_val(v, bins[b], bins[b + 1])
                    hist_bin[str(bins[b])] += p
                    hist_bin[str(bins[b + 1])] += q
        hist_bin['0'] += hist_bin['64']
        x = hist_bin.values()
        hgram = x[0:9]
        return hgram

    def calc_hist(self, img):
        hist = []
        (m, n) = img.shape
        img = img.astype("float")
        code_val = np.array((m - 2, n - 2))
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                grad_0 = img[i][j] - img[i + 1][j]
                grad_45 = img[i][j] - img[i + 1][j + 1]
                grad_90 = img[i][j] - img[i][j + 1]
                grad_135 = img[i][j] - img[i - 1][j + 1]
                vector = [self.encod(grad_0, grad_45), self.encod(grad_0, grad_90), self.encod(grad_0, grad_135),
                          self.encod(grad_45, grad_90), self.encod(grad_45, grad_135), self.encod(grad_90, grad_135)]
                val = 32 * vector[0] + 16 * vector[1] + 8 * vector[2] + 4 * vector[3] + 2 * vector[4] + vector[5]
                code_val[i-1][j-1] = val
        r = 0
        c = 0
        while r < m-1:
            while c < n-1:
                block = code_val[r:r+8][c:c+8]
                data = block.tolist()
                h = self.block_hist(data)
                hist.append(h)
                hist = [v for ele in hist for v in ele]
                c += 8
            r += 8
        return hist
