import React from 'react';
import { Bell } from 'lucide-react';

export const Notifications: React.FC = () => {
    // Mock notifications
    const notifications = [
        { id: 1, text: "Meeting with Team in 10 mins", time: "10m ago" },
        { id: 2, text: "Task 'Review PR' is overdue", time: "1h ago" }
    ];

    return (
        <div className="p-4 bg-card rounded-xl border border-border shadow-sm">
            <h3 className="font-semibold flex items-center gap-2 mb-4">
                <Bell size={18} /> Notifications
            </h3>
            <div className="space-y-3">
                {notifications.map(n => (
                    <div key={n.id} className="text-sm border-b border-border/50 pb-2 last:border-0">
                        <p className="font-medium">{n.text}</p>
                        <span className="text-xs text-muted-foreground">{n.time}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};
