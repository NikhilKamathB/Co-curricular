# https://github.com/soumilshah1995/Learn-Apache-Airflow-in-easy-way-

try:
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    import pandas as pd
    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))


def func_1(**context):
    print(f"Hello world -> Func 1 -> msg: {context['msg']}")

def func_2(**context):
    print(f"Hello world -> Func 2 -> msg: {context['msg']}")

def func_3(**context):
    print(f"Hello world -> Func 3")

with DAG(
    dag_id="first_dag",
    schedule_interval="@daily",
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 7, 20)
    },
    catchup=False
) as dag:
    func_1_execute = PythonOperator(
        task_id="func_1_func",
        python_callable=func_1,
        provide_context=True,
        op_kwargs={"msg": "This is the first function"}
    )
    func_2_execute = PythonOperator(
        task_id="func_2_func",
        python_callable=func_2,
        provide_context=True,
        op_kwargs={"msg": "This is the second function"}
    )
    func_3_execute = PythonOperator(
        task_id="func_3_func",
        python_callable=func_3,
        provide_context=True
    )

func_1_execute >> func_2_execute >> func_3_execute