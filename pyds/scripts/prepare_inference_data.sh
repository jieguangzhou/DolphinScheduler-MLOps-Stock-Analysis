export PYTHONPATH=${project}
source ${project}/env/bin/activate
python -m dmsa.data_processing.build_datas \
    --task_type inference \
    --config ${project}/feature_signal.txt \
    --save_path "${s3_inference_data_path}"
