/**
 * Reusable Alert Component
 * 
 * Displays success, error, warning, or info messages.
 */
export default function Alert({ type = 'info', message, onClose }) {
  if (!message) return null;

  const getColors = () => {
    switch (type) {
      case 'success':
        return {
          bg: '#d4edda',
          border: '#c3e6cb',
          text: '#155724'
        };
      case 'error':
        return {
          bg: '#f8d7da',
          border: '#f5c6cb',
          text: '#721c24'
        };
      case 'warning':
        return {
          bg: '#fff3cd',
          border: '#ffeaa7',
          text: '#856404'
        };
      case 'info':
      default:
        return {
          bg: '#d1ecf1',
          border: '#bee5eb',
          text: '#0c5460'
        };
    }
  };

  const colors = getColors();
  
  const getIcon = () => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✗';
      case 'warning':
        return '⚠';
      case 'info':
      default:
        return 'ℹ';
    }
  };

  const styles = {
    padding: '12px 16px',
    backgroundColor: colors.bg,
    color: colors.text,
    border: `1px solid ${colors.border}`,
    borderRadius: '4px',
    marginBottom: '16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    fontSize: '14px',
    lineHeight: '1.5'
  };

  return (
    <div style={styles}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <strong>{getIcon()}</strong>
        <span>{message}</span>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: colors.text,
            cursor: 'pointer',
            fontSize: '18px',
            padding: '0 4px',
            lineHeight: '1'
          }}
        >
          ×
        </button>
      )}
    </div>
  );
}
