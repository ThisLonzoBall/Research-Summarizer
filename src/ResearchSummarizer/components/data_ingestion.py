from datasets import Dataset, DatasetDict, load_dataset

from ResearchSummarizer.entity import DataIngestionConfig
from ResearchSummarizer.logging import logger


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_dataset(self) -> DatasetDict:
        """Stream the first N examples of each split from the Hugging Face Hub.

        Streaming avoids downloading the full ~7GB arXiv corpus when only a subset is needed.
        """
        if self.config.save_dir.exists():
            logger.info(f"Dataset already present at {self.config.save_dir}, skipping download.")
            return DatasetDict.load_from_disk(self.config.save_dir)

        splits = {}
        for split, n in self.config.split_sizes.items():
            logger.info(f"Streaming {n} examples from {self.config.dataset_name} [{split}]")
            stream = load_dataset(
                self.config.dataset_name,
                self.config.dataset_config,
                split=split,
                streaming=True,
            )
            splits[split] = Dataset.from_list(list(stream.take(n)))

        dataset = DatasetDict(splits)
        dataset.save_to_disk(self.config.save_dir)
        logger.info(f"Saved dataset to {self.config.save_dir}: {dataset}")
        return dataset
