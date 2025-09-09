function SummaryCard({ title = "Summary", body }) {
  if (!body) return null;
  return (
    <div className="card">
      <div className="card-title">{title}</div>
      <div className="card-body">{body}</div>
    </div>
  );
}

export default SummaryCard;