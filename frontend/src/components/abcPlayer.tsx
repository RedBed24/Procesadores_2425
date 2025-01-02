import abcjs, { synth } from 'abcjs';
import '../css/midi-player.css';
import { useEffect, useRef, useState } from 'react';
import { Button, Group, Center, Loader, Progress, Slider, Text, Stack, ActionIcon } from "@mantine/core";
import { Play, Pause, Settings, Square, Download } from 'lucide-react';

interface AbcPlayerProps {
    abcMusic: string;
    display: boolean
}

export const AbcPlayer: React.FC<AbcPlayerProps> = ({ abcMusic, display }) => {
    const [isInitialized, setIsInitialized] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);


    const [controler, setControler] = useState<abcjs.SynthObjectController | undefined>(undefined);
    const [visualObj, setVisualObj] = useState<abcjs.TuneObject | undefined>(undefined);
    const paperRef = useRef<HTMLDivElement | null>(null);

    const handleInit = async () => {
        try {
            setLoading(true);
            console.log('Initializing synth...');
            const contextAudio = new (window.AudioContext || (window as any).webkitAudioContext)();

            const visualObj = abcjs.renderAbc("paper", abcMusic, {
                responsive: "resize",
                add_classes: true,
            })[0];


            setIsInitialized(true);
            setError(null);

            const controler = new abcjs.synth.SynthController();

            controler.load("#audio", {}, {
                displayRestart: true,
                displayPlay: true,
                displayProgress: true,
            });
            controler.setTune(visualObj, true, {
                audioContext: contextAudio,
            }).then(() => {
                console.log("Audio successfully loaded.");
            }).catch((error) => {
                console.warn("Audio problem:", error);
            });

            const timingCallbacks = new abcjs.TimingCallbacks(visualObj, {
                beatCallback: undefined,
                lineEndCallback: undefined,
                eventCallback: handleEvent,
            });


            setControler(controler);
            setVisualObj(visualObj);

        } catch (err) {
            console.error('Error initializing synth:', err);
            setError('Failed to initialize the synthesizer.');
        }
        finally {
            setLoading(false);
        }
        setLoading(false);
    };


    const handleEvent = (ev: any) => {
        // Limpiar resaltado de notas anteriores
        document.querySelectorAll('.abcjs-note').forEach(note => note.classList.remove('highlighted'));

        if (ev && ev.elements) {
            // Resaltar las notas activas
            ev.elements.forEach((element: Element) => {
                element.classList.add('highlighted');
            });
        }
    };

    const handleBeat = (beatNumber: number, totalBeats: number, beatFraction: number) => {
        const currentNotes = document.querySelectorAll(`.abcjs-note`);
        currentNotes.forEach(note => note.classList.remove('highlighted'));

        const highlightedNotes = document.querySelectorAll(`.abcjs-note.abcjs-beat-${beatNumber}`);
        highlightedNotes.forEach(note => note.classList.add('highlighted'));
    };
    useEffect(() => {
        if (display) {
            handleInit();
        }
        const style = document.createElement('style');
        style.innerHTML = `
            .highlighted {
                fill: red !important;
                stroke: red !important;
            }
        `;
        document.head.appendChild(style);

        return () => {
            document.head.removeChild(style);
        };
    }, [display]);

    const downloadMidi = () => {
        if (controler) {
            const title = visualObj?.metaText?.title || 'music';
            controler.download(title);
        }
    };
    const handleDownload = () => {
        if (paperRef.current) {
          const svgElement = paperRef.current.querySelector('svg');
          if (svgElement) {
            // Convertir el SVG a un string
            const svgString = new XMLSerializer().serializeToString(svgElement);
    
            // Crear un Blob para el archivo SVG
            const blob = new Blob([svgString], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);
    
            // Crear un enlace de descarga y simular el clic
            const a = document.createElement('a');
            a.href = url;
            a.download = 'partitura.svg'; // Nombre del archivo descargado
            a.click();
    
            // Liberar el URL temporal
            URL.revokeObjectURL(url);
          }
        }
      };

    return (
        <>

            <Stack>
                <Group p={0}>
                    <div id="audio" style={{ flexGrow: 1, margin: 0 }} ></div>
                    <ActionIcon onClick={downloadMidi}
                        style={{
                            height: '24px',
                            padding: '0 5px',
                            borderRadius: '3px',
                            backgroundColor: '#424242',
                            margin: 0
                        }}><Download /></ActionIcon>
                </Group>
                <Stack p={0} style={{ border: '1px solid black', marginBottom: '20px', position: 'relative' }}>
                    <ActionIcon onClick={handleDownload} bg='black'
                        style={{
                            height: '24px',
                            padding: '0 5px',
                            borderRadius: '3px',
                            margin: 0,
                            position: 'absolute',
                            top: '20px',
                            right: '5px',
                            zIndex: 1
                        }}><Download /></ActionIcon>
                    <div id="paper" ref={paperRef} style={{ marginTop: 0 }} ></div>
                </Stack>
            </Stack>
        </>
    );
};