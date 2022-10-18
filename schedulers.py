from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        if cur_event.event_type == EventTypes.PROC_ARRIVES:
            return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        self.time+=cur_process.run_for(cur_process.service_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)

class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        self.processes.sort(key=lambda x: x.service_time)
        for i in self.processes:
            if i.process_state == ProcessStates.READY:
                return i

    def dispatcher_func(self, cur_process):
        self.time += cur_process.run_for(cur_process.remaining_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)

class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        if cur_event.event_type == EventTypes.PROC_ARRIVES or cur_event.event_type == EventTypes.PROC_CPU_REQ:
            return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        self.time += cur_process.run_for(self.quantum, self.time)
        if cur_process.remaining_time > 0:
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)

class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        self.processes.sort(key=lambda x: x.remaining_time)
        for i in self.processes:
            if i.process_state == ProcessStates.READY:
                return i

    def dispatcher_func(self, cur_process):
        self.time += cur_process.run_for(self.next_event_time() - self.time, self.time)
        if cur_process.remaining_time > 0:
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)