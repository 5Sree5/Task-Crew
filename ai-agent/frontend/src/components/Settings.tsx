import React from 'react';
import { Sliders } from 'lucide-react';

export const Settings: React.FC = () => {
    return (
        <div className="p-6">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Sliders /> Settings
            </h2>
            <div className="space-y-6 max-w-xl">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="font-medium">Dark Mode</h3>
                        <p className="text-sm text-muted-foreground">Toggle application theme</p>
                    </div>
                    <div className="w-10 h-6 bg-primary rounded-full relative cursor-pointer">
                        <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
                    </div>
                </div>

                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="font-medium">Email Notifications</h3>
                        <p className="text-sm text-muted-foreground">Receive daily summaries</p>
                    </div>
                    <div className="w-10 h-6 bg-muted rounded-full relative cursor-pointer">
                        <div className="absolute left-1 top-1 w-4 h-4 bg-muted-foreground rounded-full"></div>
                    </div>
                </div>

                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="font-medium">Google Calendar Sync</h3>
                        <p className="text-sm text-muted-foreground">Connected as user@demo.com</p>
                    </div>
                    <button className="text-sm text-destructive font-medium">Disconnect</button>
                </div>
            </div>
        </div>
    );
};
