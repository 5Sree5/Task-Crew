import React, { useEffect, useState } from 'react';
import api from '../api/client';
import { MoreHorizontal, Plus } from 'lucide-react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

interface Task {
    id: number;
    title: string;
    description: string;
    status: string;
    priority: string;
}

const SortableTask = ({ task }: { task: Task }) => {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: task.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    };

    return (
        <div
            ref={setNodeRef} style={{ ...style, borderLeftColor: task.priority === 'high' ? 'hsl(var(--destructive))' : task.priority === 'medium' ? 'hsl(32, 95%, 44%)' : 'hsl(var(--border))' }} {...attributes} {...listeners}
            className="bg-card p-4 rounded-xl border-l-[4px] border-y border-r border-border shadow-sm hover:shadow-lg transition-all cursor-grab group mb-4 touch-none relative overflow-hidden"
        >
            <div className="absolute top-0 right-0 p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button className="text-muted-foreground hover:text-foreground">
                    <MoreHorizontal size={16} />
                </button>
            </div>

            <h3 className="font-semibold text-base mb-1 pr-6 tracking-tight text-card-foreground">{task.title}</h3>
            {task.description && <p className="text-xs text-muted-foreground mb-3 line-clamp-2">{task.description}</p>}

            <div className="flex items-center justify-between mt-2">
                <div className="flex items-center gap-2">
                    <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${task.priority === 'high' ? 'border-red-500/20 text-red-500 bg-red-500/10' :
                        task.priority === 'medium' ? 'border-orange-500/20 text-orange-500 bg-orange-500/10' :
                            'border-gray-500/20 text-gray-500 bg-gray-500/10'
                        }`}>
                        {task.priority}
                    </span>
                </div>
                <div className="text-[10px] text-muted-foreground font-mono">ID: {task.id}</div>
            </div>
        </div>
    );
};

export const TaskBoard: React.FC = () => {
    const [tasks, setTasks] = useState<Task[]>([]);

    const fetchTasks = async () => {
        try {
            const res = await api.get('/tasks');
            setTasks(res.data);
        } catch (e) {
            console.error("Failed to fetch tasks", e);
        }
    };

    useEffect(() => {
        fetchTasks();
        const interval = setInterval(fetchTasks, 5000);
        return () => clearInterval(interval);
    }, []);

    const sensors = useSensors(
        useSensor(PointerSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    const columns = [
        { id: 'todo', title: 'To Do', color: 'bg-yellow-500/10 text-yellow-500' },
        { id: 'in-progress', title: 'In Progress', color: 'bg-blue-500/10 text-blue-500' },
        { id: 'done', title: 'Done', color: 'bg-green-500/10 text-green-500' },
    ];

    const handleDragEnd = (event: any) => {
        const { active, over } = event;

        if (!over) return;

        const activeId = active.id;
        // Simple drag logic: find the task and update its status based on the container dropped into
        // NOTE: This basic implementation assumes dropping onto a column container or another item in that column.

        // For simplicity in this demo, we'll just log the move. 
        // A robust kanban needs 'Droppable' containers for columns.
        console.log(`Dragged ${activeId} over ${over.id}`);

        // In a real app, calculate new status and call API:
        // api.post(`/tasks/${activeId}/move`, { status: newStatus });
    };

    return (
        <div className="h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Task Board</h2>
                <button className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-md hover:opacity-90">
                    <Plus size={16} /> New Task
                </button>
            </div>

            <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
                <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden">
                    {columns.map(col => {
                        const colTasks = tasks.filter(t => t.status === col.id);
                        return (
                            <div key={col.id} className="flex flex-col bg-muted/40 backdrop-blur-sm rounded-2xl p-4 border border-border/60 h-full shadow-inner">
                                <div className={`flex items-center justify-between mb-4 px-1`}>
                                    <div className="flex items-center gap-2">
                                        <div className={`w-3 h-3 rounded-full ${col.id === 'todo' ? 'bg-yellow-500' : col.id === 'in-progress' ? 'bg-blue-500' : 'bg-green-500'} shadow-[0_0_8px] shadow-current opacity-80`}></div>
                                        <span className="font-bold text-sm tracking-wide text-foreground/90">
                                            {col.title}
                                        </span>
                                    </div>
                                    <span className="bg-background/80 px-2 py-0.5 rounded-md text-[10px] font-bold text-muted-foreground border border-border/50 shadow-sm">
                                        {colTasks.length}
                                    </span>
                                </div>

                                <div className="flex-1 overflow-y-auto">
                                    <SortableContext items={colTasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
                                        {colTasks.map(task => (
                                            <SortableTask key={task.id} task={task} />
                                        ))}
                                    </SortableContext>
                                    {colTasks.length === 0 && (
                                        <div className="text-center py-8 text-muted-foreground text-sm border-2 border-dashed border-border rounded-lg">
                                            No tasks
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </DndContext>
        </div>
    );
};
