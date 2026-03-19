import subprocess
import os

boards = {
    'easy': (15, 3, 3, 7),
    'inter': (15, 3, 4, 11),
    'hard': (15, 4, 4, 20),
    'expert': (15, 5, 5, 30)
}

print("Generating boards...")
for difficulty, (count, p, q, m) in boards.items():
    os.makedirs(f'custom_boards/{difficulty}', exist_ok=True)
    subprocess.run(['python3', '../Sudoku_Generator/board_generator.py', f'custom_boards/{difficulty}/board', str(count), str(p), str(q), str(m)])

print(f"{'Board Size':<22} | {'Sample Size':<11} | {'Boards Solved':<15} | {'Average Backtracks':<20}")
print("-" * 75)

total_size = 0
total_solved = 0
total_bt = 0

for difficulty in ['easy', 'inter', 'hard', 'expert']:
    solved = 0
    total_backtracks = 0
    files = os.listdir(f'custom_boards/{difficulty}')
    for f in files:
        if not f.endswith('.txt'): continue
        try:
            # 2 second timeout per board for FC (Minimal AI)
            result = subprocess.run(['python3', 'src/Main.py', 'FC', f'custom_boards/{difficulty}/{f}'], capture_output=True, text=True, timeout=2)
            if "Failed to find a solution" not in result.stdout:
                solved += 1
                for line in result.stdout.split('\n'):
                    if 'Backtracks:' in line:
                        total_backtracks += int(line.split(':')[1].strip())
        except subprocess.TimeoutExpired:
            pass
    
    avg_bt = total_backtracks // solved if solved > 0 else "N/A (Timeout)"
    
    name_map = {'easy': '9x9 (easy)', 'inter': '12x12 (intermediate)', 'hard': '16x16 (hard)', 'expert': '25x25 (Expert)'}
    print(f"{name_map[difficulty]:<22} | {len(files):<11} | {solved:<15} | {avg_bt:<20}")
    
    total_size += len(files)
    total_solved += solved
    total_bt += total_backtracks

total_avg = total_bt // total_solved if total_solved > 0 else "N/A"
print("-" * 75)
print(f"{'Total Summary':<22} | {total_size:<11} | {total_solved:<15} | {total_avg:<20}")
