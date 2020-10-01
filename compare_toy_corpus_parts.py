import pyitlib.discrete_random_variable as drv
from numpy.lib.stride_tricks import as_strided
import numpy as np
import matplotlib.pyplot as plt

from preppy import PartitionedPrep


from grokkingsvd.corpus_toy import ToyCorpus
from grokkingsvd.figs import plot_singular_values, make_example_fig


tc = ToyCorpus()
prep = PartitionedPrep(tc.docs,
                       reverse=False,
                       num_types=tc.num_types,
                       num_parts=2,
                       num_iterations=(1, 1),
                       batch_size=64,
                       context_size=1)
test_words = [p for p in tc.nouns if p in prep.store.w2id]
test_word_ids = [prep.store.w2id[w] for w in test_words]

s_list = []
num_sv = 8
for part_id, part in enumerate(prep.reordered_parts):

    # windows
    token_ids_array = part.astype(np.int64)
    num_possible_windows = len(token_ids_array) - prep.num_tokens_in_window
    shape = (num_possible_windows, prep.num_tokens_in_window)
    windows = as_strided(token_ids_array, shape, strides=(8, 8), writeable=False)

    # windows with probe in position -2
    row_ids = np.isin(windows[:, -2], test_word_ids)
    probe_windows = windows[row_ids]

    # conditional entropy
    x = probe_windows[:, -2]  # CAT member
    y = probe_windows[:, -1]  # next-word
    x_y = np.vstack((x, y))   # joint outcome

    # map word ID of nouns to IDs between [0, len(test_words)]
    # this makes creating a matrix with the right number of columns easier
    x2x = {xi: n for n, xi in enumerate(np.unique(x))}

    # make co-occurrence plot
    cf_mat = np.ones((prep.num_types, len(x2x))) * 1e-9
    for xi, yi in zip(x, y):
        cf_mat[yi, x2x[xi]] += 1
    last_num_rows = tc.num_types - tc.num_nouns  # other rows are just empty because of nouns not occurring with nouns
    fig, ax = make_example_fig(np.log(cf_mat[-last_num_rows:]))
    ce = drv.entropy_conditional(x, y).item()
    je = drv.entropy_joint(x_y).item()
    ye = drv.entropy_joint(y).item()
    plt.title(f'Toy Corpus Part {part_id+1}\nH(noun|slot 2)={ce:.4f}\nH(noun,slot 2)={je:.4f}\nH(slot 2)={ye:.4f}')
    plt.show()

    print(np.sum(np.var(cf_mat, axis=0)))  # row-wise variance is higher for part 1
    print(np.sum(np.var(cf_mat, axis=1)))
    print(np.sum(cf_mat))

    # SVD
    s = np.linalg.svd(cf_mat, compute_uv=False)
    print(f'first {num_sv} singular values', ' '.join(['{:>6.2f}'.format(si) for si in s[:num_sv]]))
    s_list.append(np.asarray(s[:num_sv]))

plot_singular_values(s_list, max_s=num_sv)

