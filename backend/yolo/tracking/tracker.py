class BOTSORTArgs(object):
    track_high_thresh = 0.5  # threshold for the first association
    track_low_thresh = 0.1  # threshold for the second association
    new_track_thresh = 0.6  # threshold for init new track if the detection does not match any tracks
    track_buffer = 30  # buffer to calculate the time when to remove tracks
    match_thresh = 0.8  # threshold for matching tracks

    gmc_method = "sparseOptFlow"

    proximity_thresh = 0.5
    appearance_thresh = 0.25
    fuse_score = True
    with_reid = True
