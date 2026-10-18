function SummaryCard({ title = "Summary", body }) {
  if (!body) return null;

  return (
    <div className="border rounded-2xl p-4 shadow-sm bg-white">
      <div className="text-base font-semibold mb-2">{title}</div>
      <div className="text-base leading-relaxed whitespace-pre-line break-words">
        {body}
      </div>
    </div>
  );
}

export default SummaryCard;