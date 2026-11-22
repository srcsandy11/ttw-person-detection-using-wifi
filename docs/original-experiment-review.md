# Review of the existing PPD experiments

The supplied project contains a capture logger, public dataset adapters, a synthetic generator, preprocessing, training and prediction, evaluation scripts, saved metrics, and a demonstration viewer. The folder contains no raw session captures or trained checkpoints. The original experiments and the new benchmark both use BUET, so this is a new model and evaluation protocol on a previously explored source.

* In results/metrics_R5_final.json the reported presence macro-F1 is 0.903 on 489 windows. The count confusion matrix has true labels only for 0 and 1. The saved run supplies no measured accuracy for two or more occupants.
* In public_adapters.py BUET “day” is derived from the subject identifier for occupied records and from the filename for empty records. A split on “day” here does not demonstrate transfer across actual calendar days.
* experiments/run_rounds.sh uses S03 in round-four training while selecting configurations, then calls S03 the final holdout in round five. The round-six alternatives also reuse that holdout. A new room and new sessions are needed for an independent final result.
* train.py estimates hourly false alarms from the fraction of empty windows flagged multiplied by 3600 / window length. This is a window-based extrapolation. A deployment evaluation should count the starts of distinct false-alarm episodes and divide by actual empty-room observation time.
* autotune.py uses validation reward to search hyperparameters with the cross-entropy method. New labeled sessions support supervised retraining. Repeatedly fitting the same recordings adds no independent evidence.
* A synthetic room visualization checks display behavior. Physical validation requires independently recorded ground truth and predictions synchronized to the same time base.

The single-receiver benchmark uses only source RX1 features, complete recording splits and train-only scaling. Its scores cannot be compared directly with the original CNN scores because the features, windows and metrics differ. Use a fresh room for the next test, and report false alarms and misses separately for each room.
