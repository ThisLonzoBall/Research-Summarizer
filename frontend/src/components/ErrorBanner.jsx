function ErrorBanner({ message, onClose }) {
  if (!message) return null;
  return (
    <div className="error">
      <div>{message}</div>
      {onClose && (
        <button
          style={{
            marginLeft: 12,
            border: "none",
            background: "transparent",
            cursor: "pointer",
          }}
          onClick={onClose}
        >
          ✕
        </button>
      )}
    </div>
  );
}

export default ErrorBanner;