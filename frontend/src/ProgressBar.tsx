import { useRef } from "react";
import { CSSTransition } from "react-transition-group";

interface ProgressBarParams {
  active: boolean;
}

export function ProgressBar({ active }: ProgressBarParams): JSX.Element {
  const nodeRef = useRef(null);
  return (
    <div className="flex h-2 overflow-hidden bg-white border-t border-b border-white">
      <CSSTransition
        nodeRef={nodeRef}
        in={active}
        timeout={999999}
        classNames={{
          enter: "w-0",
          enterActive: "w-full duration-long",
        }}
      >
        <div
          ref={nodeRef}
          className="bg-yellow-500 shadow-none transition-all ease-linear"
        ></div>
      </CSSTransition>
    </div>
  );
}
