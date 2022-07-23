export PYTHONPATH=${project}
source ${project}/env/bin/activate
python -m dmsa.data_processing.build_datas \
    --task_type train \
    --config ${project}/feature_signal.txt \
    --save_path "${s3_data_path}" \
    --data_path ${project}/data/daily
