from argparse import ArgumentParser

EMPATH_INITIALS = ['A','B','W','H']
EMPATH_POSSIBLE_DATA_PATHS = ['./articles/2018/byrace/A', './articles/2018/byrace/B', './articles/2018/byrace/W', './articles/2018/byrace/H']
EMPATH_POSSIBLE_LABELS = ['Asian', 'Black', 'White', 'Hispanic']


LIWC_INITIALS = ['W','H','B','A']
LIWC_POSSIBLE_LABELS = ['White', 'Hispanic', 'Black','Asian']
LIWC_POSSIBLE_FILENAMES = ['W.txt', 'H.txt', 'B.txt', 'A.txt']

def get_empath_options(description):
    parser = ArgumentParser(description=description)
    parser.add_argument("--races", default='ABWH', help="Enter as one combined string (ex. --races BW to include black and white). Options: A:Asian, B:Black, W:White, H:Hispanic. Default is all")
    parser.add_argument("--num", type=int, default=7, help="number of metrics (cateogories) to graph on the x axis. default is 7")

    args = parser.parse_args()
    num_metrics = args.num
    selected_races = args.races.upper()

    data_paths = [EMPATH_POSSIBLE_DATA_PATHS[i] for i in range(len(EMPATH_POSSIBLE_DATA_PATHS)) if EMPATH_INITIALS[i] in selected_races]
    labels = [EMPATH_POSSIBLE_LABELS[i] for i in range(len(EMPATH_POSSIBLE_LABELS)) if EMPATH_INITIALS[i] in selected_races]

    return (data_paths, labels, num_metrics)

def get_liwc_options(description):


    parser = ArgumentParser(description=description)
    parser.add_argument("--races", default='ABWH', help="Enter as one combined string (ex. --races BW to include black and white). Options: A:Asian, B:Black, W:White, H:Hispanic. Default is all")
    parser.add_argument("--num", type=int, default=7, help="number of metrics (cateogories) to graph on the x axis. default is 7")

    args = parser.parse_args()
    num_metrics = args.num
    selected_races = args.races.upper()

    filenames = [LIWC_POSSIBLE_FILENAMES[i] for i in range(len(LIWC_POSSIBLE_FILENAMES)) if LIWC_INITIALS[i] in selected_races]
    labels = [LIWC_POSSIBLE_LABELS[i] for i in range(len(LIWC_POSSIBLE_LABELS)) if LIWC_INITIALS[i] in selected_races]
    num_metrics = num_metrics

    return (filenames, labels, num_metrics)
