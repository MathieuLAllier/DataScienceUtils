import math


def sample_size(effect, conversion, significance=0.95):
    """
    https://gist.github.com/kdzwinel/201293d7e35981e87b40
    :param effect: Minimum Detectable Effect
    :param conversion: Baseline Conversion Rate
    :param significance:
    :param power:
    :return: sample size
    """
    c = conversion - (conversion + effect)
    p = math.fabs(conversion * effect)
    o = conversion * (1 - conversion) + c * (1 - c)
    s_size = math.ceil(2 * significance * o * math.log(1 + math.sqrt(o) / p) / (p * p))
    print('Sample size of {:,}'.format(s_size))
    return s_size


def test_run_time(sample, average_daily_user, n_variation):
    assert n_variation > 1, 'Number of variation should be higher than 1'
    return sample / (average_daily_user / n_variation)


if __name__ == '__main__':
    print(test_run_time(sample_size(0.03, 0.10), 5000, 2))
