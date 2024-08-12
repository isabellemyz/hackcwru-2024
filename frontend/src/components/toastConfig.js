import { Slide, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const toastConfig = {
  position: "bottom-center",
  autoClose: 1400,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  progress: undefined,
  transition: Slide,
};

export const showToast = (message, type = 'default') => {
  switch (type) {
    case 'success':
      toast.success(message, toastConfig);
      break;
    case 'error':
      toast.error(message, toastConfig);
      break;
    case 'info':
      toast.info(message, toastConfig);
      break;
    case 'warning':
      toast.warn(message, toastConfig);
      break;
    default:
      toast(message, toastConfig);
      break;
  }
};

