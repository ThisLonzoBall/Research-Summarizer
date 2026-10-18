from pathlib import Path

from ResearchSummarizer.config.configuration import ConfigurationManager

ROOT = Path(__file__).resolve().parents[1]


def test_all_stage_configs_load(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # artifact directories are created relative to cwd
    cm = ConfigurationManager(ROOT / "config" / "config.yaml", ROOT / "params.yaml")

    ingestion = cm.get_data_ingestion_config()
    transformation = cm.get_data_transformation_config()
    trainer = cm.get_model_trainer_config()
    evaluation = cm.get_model_evaluation_config()

    # Each stage reads what the previous one writes.
    assert transformation.data_path == ingestion.save_dir
    assert trainer.data_path == transformation.save_dir
    assert evaluation.model_path == trainer.model_dir
    assert set(ingestion.split_sizes) == {"train", "validation", "test"}
    assert "eval_strategy" in trainer.training_args
