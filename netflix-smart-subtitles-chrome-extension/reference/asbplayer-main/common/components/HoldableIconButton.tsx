import IconButton, { IconButtonProps } from '@mui/material/IconButton';
import React, { useEffect, useCallback, useState } from 'react';
import { isMobile } from 'react-device-detect';

interface Props extends IconButtonProps {
    onHold?: (repetition: number) => void;
    onClick: () => void;
    children: React.ReactNode;
}

const HoldableIconButton = ({ onHold, onClick, children, ...rest }: Props) => {
    const [startTime, setStartTime] = useState<number>();

    const repetitions = useCallback(() => {
        if (startTime === undefined) {
            return undefined;
        }

        const holdTime = Date.now() - startTime;
        return holdTime / 250;
    }, [startTime]);

    const handleMouseUp = () => {
        const reps = repetitions();

        if (reps !== undefined && reps < 1) {
            onClick?.();
        }

        setStartTime(undefined);
    };

    const handleMouseDown = () => {
        setStartTime(Date.now());
    };

    useEffect(() => {
        if (startTime === undefined) {
            return;
        }

        const interval = setInterval(() => {
            const reps = repetitions();

            if (reps !== undefined && reps > 0) {
                onHold?.(reps);
            }
        }, 250);
        return () => clearInterval(interval);
    }, [startTime, onHold, repetitions]);
    return (
        <>
            {isMobile && (
                <IconButton onTouchStart={handleMouseDown} onTouchEnd={handleMouseUp} onClick={() => {}} {...rest}>
                    {children}
                </IconButton>
            )}
            {!isMobile && (
                <IconButton onMouseDown={handleMouseDown} onMouseUp={handleMouseUp} onClick={() => {}} {...rest}>
                    {children}
                </IconButton>
            )}
        </>
    );
};

export default HoldableIconButton;
