from .models import ModelProcess, StefanProblem


MODEL_PROCESS_TASK = ModelProcess()
STEFAN_PROBLEM_TASK = StefanProblem()

wolfram_tasks = {
    MODEL_PROCESS_TASK.id: MODEL_PROCESS_TASK,
    STEFAN_PROBLEM_TASK.id: STEFAN_PROBLEM_TASK,
}
