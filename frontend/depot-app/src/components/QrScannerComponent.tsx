import React, { useState, useEffect, useRef } from 'react';
import QrScanner from 'qr-scanner';
import { Box } from 'grommet';

export const QrScannerComponent: React.FC = () => {
    const [data, setData] = useState<string | null>(null);
    const videoRef = useRef<HTMLVideoElement | null>(null);

    useEffect(() => {
        if (videoRef.current) {
            const qrScanner = new QrScanner(
                videoRef.current,
                result => setData(result.data),
                {
                    onDecodeError: error => console.info(error),
                }
            );
            qrScanner.start();

            return () => {
                qrScanner.stop();
            };
        }
    }, [videoRef]);

    return (
        <Box gap="medium">
            <video ref={videoRef} style={{ width: '100%' }} />
            <p>{data ? `Scanned Data: ${data}` : 'No data scanned yet'}</p>
        </Box>
    );
};

export default QrScannerComponent;