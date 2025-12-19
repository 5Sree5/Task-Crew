import React, { useEffect, useState } from 'react';
import api from '../api/client';
import { MapPin } from 'lucide-react';
import { format, parseISO } from 'date-fns';

interface Event {
    id: number;
    title: string;
    start_time: string;
    end_time: string;
    location: string;
    description: string;
}

export const CalendarView: React.FC = () => {
    const [events, setEvents] = useState<Event[]>([]);

    const fetchEvents = async () => {
        try {
            const res = await api.get('/calendar/events');
            setEvents(res.data.sort((a: any, b: any) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime()));
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        fetchEvents();
        const interval = setInterval(fetchEvents, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Today's Schedule</h2>
                <div className="text-sm text-muted-foreground">
                    {format(new Date(), 'EEEE, MMMM do, yyyy')}
                </div>
            </div>

            <div className="flex-1 bg-muted/30 rounded-xl border border-border/50 p-4 overflow-y-auto relative">
                {/* Simple vertical timeline */}
                <div className="absolute left-8 top-4 bottom-4 w-px bg-border"></div>

                <div className="space-y-6">
                    {events.length === 0 ? (
                        <div className="ml-12 text-muted-foreground">No events scheduled.</div>
                    ) : (
                        events.map((event) => (
                            <div key={event.id} className="relative flex gap-4 ml-2">
                                <div className="absolute -left-2.5 mt-1 w-5 h-5 rounded-full border-4 border-background bg-primary"></div>
                                <div className="ml-8 bg-card p-4 rounded-lg border border-border shadow-sm flex-1">
                                    <div className="flex justify-between items-start">
                                        <h3 className="font-semibold text-lg">{event.title}</h3>
                                        <span className="text-xs bg-muted px-2 py-1 rounded text-foreground font-mono">
                                            {format(parseISO(event.start_time), 'HH:mm')} - {format(parseISO(event.end_time), 'HH:mm')}
                                        </span>
                                    </div>
                                    {event.location && (
                                        <div className="flex items-center gap-1 text-sm text-muted-foreground mt-1">
                                            <MapPin size={14} /> {event.location}
                                        </div>
                                    )}
                                    {event.description && (
                                        <p className="text-sm text-muted-foreground mt-2">{event.description}</p>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};
