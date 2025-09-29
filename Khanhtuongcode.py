import pandas as pd # S? d?ng th? vi?n pandas ?? hi?n th? k?t qu? d??i d?ng b?ng ??p h?n (t�y ch?n)

def round_robin(processes, quantum):
    """
    Th?c hi?n ?i?u ph?i ti?n tr�nh Round Robin v� t�nh to�n c�c ch? s? hi?u su?t.

    Args:
        processes (list of list): Danh s�ch c�c ti?n tr�nh. 
                                  M?i ti?n tr�nh: [ID, Arrival Time, Burst Time]
        quantum (int): L�t c?t th?i gian (Time Quantum).
    """
    
    # 1. Kh?i t?o d? li?u
    
    # T?o b?n sao d? li?u v� c�c c?u tr�c theo d�i
    num_processes = len(processes)
    # arrival_time: Th?i gian ??n c?a ti?n tr�nh (Gi? ??nh t?t c? ??n t?i t=0 cho ??n gi?n)
    # burst_time: Th?i gian CPU c?n thi?t ban ??u
    # completion_time: Th?i gian ho�n th�nh
    # remaining_time: Th?i gian CPU c�n l?i
    
    # S? d?ng dictionary ?? l?u tr?ng th�i c?a m?i ti?n tr�nh
    p_data = {}
    for i, p in enumerate(processes):
        pid, at, bt = p
        p_data[pid] = {
            'arrival_time': at,
            'burst_time': bt,
            'remaining_time': bt,
            'completion_time': 0,
            'start_time': -1  # Ghi l?i th?i ?i?m b?t ??u ch?y l?n ??u
        }

    # H�ng ??i s?n s�ng (Ready Queue)
    # Ban ??u, th�m t?t c? ti?n tr�nh ??n t?i th?i ?i?m 0 (Gi? ??nh ??n gi?n)
    queue = [p[0] for p in processes if p[1] == 0] 
    
    # H�ng ??i c�c ti?n tr�nh c�n l?i ch?a ??n (N?u c� th?i gian ??n > 0)
    # Ta s? gi? ??nh ??n gi?n: T?t c? ??n t?i t=0
    # N?u c?n x? l� Arrival Time > 0, logic th�m v�o queue s? ph?c t?p h?n.
    
    current_time = 0
    gantt_chart = [] # D?ng: [(Process_ID, start_time, end_time)]

    print(f"B?t ??u ?i?u ph?i Round Robin v?i Quantum = {quantum}\n")

    # 2. V�ng l?p ?i?u ph?i
    while queue or any(d['remaining_time'] > 0 for d in p_data.values()):
        
        # X? l� tr??ng h?p h�ng ??i r?ng nh?ng v?n c�n ti?n tr�nh ch?a ho�n th�nh 
        # (Ch? x?y ra n?u c� Arrival Time > current_time)
        if not queue and any(d['remaining_time'] > 0 for d in p_data.values()):
            current_time += 1
            # Th�m c�c ti?n tr�nh m?i ??n v�o h�ng ??i (N?u c�)
            # *Ph?n n�y ???c l??c b? ?? ??n gi?n, gi? ??nh t?t c? ??n t=0*
            continue

        if not queue:
            # H�ng ??i r?ng v� kh�ng c�n ti?n tr�nh n�o ?ang ch?
            break

        # L?y ti?n tr�nh ? ??u h�ng ??i
        current_pid = queue.pop(0)
        p_info = p_data[current_pid]
        
        current_remaining_time = p_info['remaining_time']
        
        # ?�nh d?u th?i ?i?m b?t ??u ch?y l?n ??u (First run)
        if p_info['start_time'] == -1:
            p_info['start_time'] = current_time

        # X�c ??nh th?i gian th?c hi?n
        execution_time = min(quantum, current_remaining_time)

        # C?p nh?t th?i gian h? th?ng v� th?i gian c�n l?i
        start_time_slice = current_time
        current_time += execution_time
        end_time_slice = current_time
        
        p_info['remaining_time'] -= execution_time

        # Ghi l?i vi?c th?c thi
        gantt_chart.append((current_pid, start_time_slice, end_time_slice))

        print(f"[{start_time_slice}-{end_time_slice}] Ti?n tr�nh {current_pid} th?c thi ({execution_time} ??n v? th?i gian). "
              f"C�n l?i: {p_info['remaining_time']}")

        # 3. T�i ?i?u ph?i
        
        # N?u ti?n tr�nh HO�N TH�NH
        if p_info['remaining_time'] == 0:
            p_info['completion_time'] = current_time
            print(f"   -> TI?N TR�NH {current_pid} HO�N TH�NH t?i t={current_time}")
            
        # N?u ti?n tr�nh CH?A HO�N TH�NH
        elif p_info['remaining_time'] > 0:
            # Th�m n� tr? l?i cu?i h�ng ??i
            queue.append(current_pid)
            
        # Ki?m tra v� th�m c�c ti?n tr�nh m?i ??n v�o h�ng ??i (N?u c�)
        # *Ph?n n�y ???c l??c b? ?? ??n gi?n, gi? ??nh t?t c? ??n t=0*


    print("\n--- K?T TH�C ?I?U PH?I ---")
    
    # 4. T�nh to�n c�c ch? s? hi?u su?t
    results = []
    total_turnaround_time = 0
    total_waiting_time = 0
    
    for pid, info in p_data.items():
        # Th?i gian Quay v�ng (Turnaround Time): Th?i gian ho�n th�nh - Th?i gian ??n
        turnaround_time = info['completion_time'] - info['arrival_time']
        
        # Th?i gian Ch? (Waiting Time): Th?i gian Quay v�ng - Th?i gian b�ng n?
        waiting_time = turnaround_time - info['burst_time']
        
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
        
        results.append({
            "ID": pid,
            "AT (??n)": info['arrival_time'],
            "BT (B�ng n?)": info['burst_time'],
            "CT (Ho�n th�nh)": info['completion_time'],
            "TAT (Quay v�ng)": turnaround_time,
            "WT (Ch?)": waiting_time
        })

    # Hi?n th? k?t qu?
    df = pd.DataFrame(results)
    
    print("\nB?NG K?T QU? HI?U SU?T:")
    print(df.to_markdown(index=False)) # D�ng to_markdown ?? hi?n th? b?ng ??p trong console
    
    avg_tat = total_turnaround_time / num_processes
    avg_wt = total_waiting_time / num_processes
    
    print(f"\nT?ng th?i gian m� ph?ng (Make Span): {current_time}")
    print(f"Th?i gian Quay v�ng Trung b�nh (Avg TAT): {avg_tat:.2f}")
    print(f"Th?i gian Ch? Trung b�nh (Avg WT): {avg_wt:.2f}")
    
    # print("\nBi?u ?? Gantt (Process_ID, Start, End):", gantt_chart)

# --- D? li?u ??u v�o ---
# ??nh d?ng: [ID_Ti?n_tr�nh, Arrival_Time (Th?i gian ??n), Burst_Time (Th?i gian b�ng n?)]
# Gi? ??nh t?t c? ??n c�ng l�c (t=0) cho v� d? ??n gi?n.
processes_data = [
    ["P1", 0, 10],
    ["P2", 0, 5],
    ["P3", 0, 8]
]

TIME_QUANTUM = 4

# Th?c thi h�m
if __name__ == '__main__':
    # Ki?m tra xem pandas c� ???c c�i ??t kh�ng
    try:
        round_robin(processes_data, TIME_QUANTUM)
    except NameError:
        print("\n*L?i: C?n c�i ??t th? vi?n 'pandas' ?? hi?n th? b?ng k?t qu? ??p.")
        print("Vui l�ng ch?y l?nh: 'pip install pandas'")
        print("N?u kh�ng mu?n d�ng pandas, b?n c� th? t? in k?t qu? t? dictionary p_data.")