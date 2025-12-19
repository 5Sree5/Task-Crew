import { AIChat } from '../components/AIChat';
import { TaskBoard } from '../components/TaskBoard';
import { CalendarView } from '../components/CalendarView';
import { Settings as SettingsComponent } from '../components/Settings';
import { Calendar, CheckSquare, Settings, LogOut } from 'lucide-react';
import { cn } from '../lib/utils';
import React, { useState } from 'react';

export const Dashboard: React.FC = () => {
    const [activeTab, setActiveTab] = useState<'board' | 'calendar' | 'settings'>('board');

    return (
        <div className="flex h-screen bg-background text-foreground font-sans">
            {/* Sidebar */}
            <div className="w-64 border-r border-border/60 p-4 flex flex-col bg-card/50 backdrop-blur-xl shadow-xl z-10">
                <div className="flex items-center gap-2 px-2 mb-8 mt-2">
                    <div className="w-9 h-9 bg-gradient-to-br from-primary to-primary/80 rounded-xl shadow-lg shadow-primary/20 flex items-center justify-center transform transition-transform hover:scale-105 duration-300">
                        <span className="text-primary-foreground font-bold text-lg">AI</span>
                    </div>
                    <h1 className="text-xl font-bold tracking-tight">Task<span className="text-primary">Master</span></h1>
                </div>

                <nav className="space-y-1 flex-1">
                    <button
                        onClick={() => setActiveTab('board')}
                        className={cn(
                            "w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                            activeTab === 'board' ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:bg-muted"
                        )}
                    >
                        <CheckSquare size={18} /> Tasks
                    </button>
                    <button
                        onClick={() => setActiveTab('calendar')}
                        className={cn(
                            "w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                            activeTab === 'calendar' ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:bg-muted"
                        )}
                    >
                        <Calendar size={18} /> Schedule
                    </button>
                    <button
                        onClick={() => setActiveTab('settings')}
                        className={cn(
                            "w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                            activeTab === 'settings' ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:bg-muted"
                        )}
                    >
                        <Settings size={18} /> Settings
                    </button>
                </nav>

                <div className="pt-4 border-t border-border space-y-1">
                    <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-destructive hover:bg-destructive/10">
                        <LogOut size={18} /> Sign Out
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex overflow-hidden">
                {/* Central Workspace */}
                <div className="flex-1 p-6 overflow-hidden">
                    {activeTab === 'board' && <TaskBoard />}
                    {activeTab === 'calendar' && <CalendarView />}
                    {activeTab === 'settings' && <SettingsComponent />}
                </div>

                {/* Right Panel - AI Chat */}
                <div className="w-[400px] border-l border-border bg-card p-4">
                    <AIChat />
                </div>
            </div>
        </div>
    );
};
