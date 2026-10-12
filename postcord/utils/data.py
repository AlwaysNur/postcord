from pathlib import Path
import pickle

def get_project_root():
    current_path = Path(__file__).resolve()

    for parent in [current_path] + list(current_path.parents):
        if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
            return parent
            
    return current_path.parent

root = get_project_root()
data_dir = root / "data"
data_dir.mkdir(exist_ok=True)

pickle_path = data_dir / "postcord.pkl"
if not pickle_path.exists():
    with pickle_path.open("wb") as file:
        pickle.dump("", file)