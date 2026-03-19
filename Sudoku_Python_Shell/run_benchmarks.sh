echo "=== MINIMAL AI (FC) ==="
for level in easy inter hard expert; do
    echo "Running Minimal AI on $level boards..."
    python3 src/Main.py FC boards/$level | tail -n 3
done

echo ""
echo "=== FINAL AI (TOURN) ==="
for level in easy inter hard expert; do
    echo "Running Final AI on $level boards..."
    python3 src/Main.py TOURN boards/$level | tail -n 3
done
