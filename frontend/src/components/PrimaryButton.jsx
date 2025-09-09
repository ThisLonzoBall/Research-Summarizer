function PrimaryButton({ disabled, onClick, children }) {
  return (
    <button className="primary" disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}

export default PrimaryButton;