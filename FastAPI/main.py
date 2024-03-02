from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for tasks (replace with database in production)
tasks = []

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    """Get all tasks"""
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    """Get a specific task by ID"""
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    """Create a new task"""
    task_dict = task.dict()
    tasks.append(task_dict)
    return task_dict

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    """Update an existing task"""
    task_index = next((index for index, task in enumerate(tasks) if task['id'] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_index] = updated_task.dict()
    return updated_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete an existing task"""
    task_index = next((index for index, task in enumerate(tasks) if task['id'] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_index]
    return {"message": "Task deleted"}
