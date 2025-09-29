import pandas as pd # S? d?ng th? vi?n pandas ?? hi?n th? k?t qu? d??i d?ng b?ng ??p h?n (tùy ch?n)

def round_robin(processes, quantum):
    """
    Th?c hi?n ?i?u ph?i ti?n trình Round Robin và tính toán các ch? s? hi?u su?t.

    Args:
        processes (list of list): Danh sách các ti?n trình. 
                                  M?i ti?n trình: [ID, Arrival Time, Burst Time]
        quantum (int): Lát c?t th?i gian (Time Quantum).
    """
    
    # 1. Kh?i t?o d? li?u
    
    # T?o b?n sao d? li?u và các c?u trúc theo dõi
    num_processes = len(processes)
    # arrival_time: Th?i gian ??n c?a ti?n trình (Gi? ??nh t?t c? ??n t?i t=0 cho ??n gi?n)
    # burst_time: Th?i gian CPU c?n thi?t ban ??u
    # completion_time: Th?i gian hoàn thành
    # remaining_time: Th?i gian CPU còn l?i
    
    # S? d?ng dictionary ?? l?u tr?ng thái c?a m?i ti?n trình
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

    # Hàng ??i s?n sàng (Ready Queue)
    # Ban ??u, thêm t?t c? ti?n trình ??n t?i th?i ?i?m 0 (Gi? ??nh ??n gi?n)
    queue = [p[0] for p in processes if p[1] == 0] 
    
    # Hàng ??i các ti?n trình còn l?i ch?a ??n (N?u có th?i gian ??n > 0)
    # Ta s? gi? ??nh ??n gi?n: T?t c? ??n t?i t=0
    # N?u c?n x? lý Arrival Time > 0, logic thêm vào queue s? ph?c t?p h?n.
    
    current_time = 0
    gantt_chart = [] # D?ng: [(Process_ID, start_time, end_time)]

    print(f"B?t ??u ?i?u ph?i Round Robin v?i Quantum = {quantum}\n")

    # 2. Vòng l?p ?i?u ph?i
    while queue or any(d['remaining_time'] > 0 for d in p_data.values()):
        
        # X? lý tr??ng h?p hàng ??i r?ng nh?ng v?n còn ti?n trình ch?a hoàn thành 
        # (Ch? x?y ra n?u có Arrival Time > current_time)
        if not queue and any(d['remaining_time'] > 0 for d in p_data.values()):
            current_time += 1
            # Thêm các ti?n trình m?i ??n vào hàng ??i (N?u có)
            # *Ph?n này ???c l??c b? ?? ??n gi?n, gi? ??nh t?t c? ??n t=0*
            continue

        if not queue:
            # Hàng ??i r?ng và không còn ti?n trình nào ?ang ch?
            break

        # L?y ti?n trình ? ??u hàng ??i
        current_pid = queue.pop(0)
        p_info = p_data[current_pid]
        
        current_remaining_time = p_info['remaining_time']
        
        # ?ánh d?u th?i ?i?m b?t ??u ch?y l?n ??u (First run)
        if p_info['start_time'] == -1:
            p_info['start_time'] = current_time

        # Xác ??nh th?i gian th?c hi?n
        execution_time = min(quantum, current_remaining_time)

        # C?p nh?t th?i gian h? th?ng và th?i gian còn l?i
        start_time_slice = current_time
        current_time += execution_time
        end_time_slice = current_time
        
        p_info['remaining_time'] -= execution_time

        # Ghi l?i vi?c th?c thi
        gantt_chart.append((current_pid, start_time_slice, end_time_slice))

        print(f"[{start_time_slice}-{end_time_slice}] Ti?n trình {current_pid} th?c thi ({execution_time} ??n v? th?i gian). "
              f"Còn l?i: {p_info['remaining_time']}")

        # 3. Tái ?i?u ph?i
        
        # N?u ti?n trình HOÀN THÀNH
        if p_info['remaining_time'] == 0:
            p_info['completion_time'] = current_time
            print(f"   -> TI?N TRÌNH {current_pid} HOÀN THÀNH t?i t={current_time}")
            
        # N?u ti?n trình CH?A HOÀN THÀNH
        elif p_info['remaining_time'] > 0:
            # Thêm nó tr? l?i cu?i hàng ??i
            queue.append(current_pid)
            
        # Ki?m tra và thêm các ti?n trình m?i ??n vào hàng ??i (N?u có)
        # *Ph?n này ???c l??c b? ?? ??n gi?n, gi? ??nh t?t c? ??n t=0*


    print("\n--- K?T THÚC ?I?U PH?I ---")
    
    # 4. Tính toán các ch? s? hi?u su?t
    results = []
    total_turnaround_time = 0
    total_waiting_time = 0
    
    for pid, info in p_data.items():
        # Th?i gian Quay vòng (Turnaround Time): Th?i gian hoàn thành - Th?i gian ??n
        turnaround_time = info['completion_time'] - info['arrival_time']
        
        # Th?i gian Ch? (Waiting Time): Th?i gian Quay vòng - Th?i gian bùng n?
        waiting_time = turnaround_time - info['burst_time']
        
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
        
        results.append({
            "ID": pid,
            "AT (??n)": info['arrival_time'],
            "BT (Bùng n?)": info['burst_time'],
            "CT (Hoàn thành)": info['completion_time'],
            "TAT (Quay vòng)": turnaround_time,
            "WT (Ch?)": waiting_time
        })

    # Hi?n th? k?t qu?
    df = pd.DataFrame(results)
    
    print("\nB?NG K?T QU? HI?U SU?T:")
    print(df.to_markdown(index=False)) # Dùng to_markdown ?? hi?n th? b?ng ??p trong console
    
    avg_tat = total_turnaround_time / num_processes
    avg_wt = total_waiting_time / num_processes
    
    print(f"\nT?ng th?i gian mô ph?ng (Make Span): {current_time}")
    print(f"Th?i gian Quay vòng Trung bình (Avg TAT): {avg_tat:.2f}")
    print(f"Th?i gian Ch? Trung bình (Avg WT): {avg_wt:.2f}")
    
    # print("\nBi?u ?? Gantt (Process_ID, Start, End):", gantt_chart)

# --- D? li?u ??u vào ---
# ??nh d?ng: [ID_Ti?n_trình, Arrival_Time (Th?i gian ??n), Burst_Time (Th?i gian bùng n?)]
# Gi? ??nh t?t c? ??n cùng lúc (t=0) cho ví d? ??n gi?n.
processes_data = [
    ["P1", 0, 10],
    ["P2", 0, 5],
    ["P3", 0, 8]
]

TIME_QUANTUM = 4

# Th?c thi hàm
if __name__ == '__main__':
    # Ki?m tra xem pandas có ???c cài ??t không
    try:
        round_robin(processes_data, TIME_QUANTUM)
    except NameError:
        print("\n*L?i: C?n cài ??t th? vi?n 'pandas' ?? hi?n th? b?ng k?t qu? ??p.")
        print("Vui lòng ch?y l?nh: 'pip install pandas'")
        print("N?u không mu?n dùng pandas, b?n có th? t? in k?t qu? t? dictionary p_data.")