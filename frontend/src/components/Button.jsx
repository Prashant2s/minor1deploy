/**
 * Reusable Button Component
 * Provides consistent button styling across the application.
 */
export default function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  type = 'button',
  fullWidth = false,
  style = {},
}) {
  const variants = {
    primary: '#007bff',
    success: '#28a745',
    danger: '#dc3545',
    info: '#17a2b8',
    secondary: '#6c757d',
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: '8px 16px',
        backgroundColor: variants[variant] || variants.primary,
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        fontSize: '14px',
        fontWeight: '500',
        opacity: disabled ? 0.6 : 1,
        width: fullWidth ? '100%' : 'auto',
        ...style,
      }}
    >
      {children}
    </button>
  );
}
