import abcjs, { synth } from 'abcjs';
import '../css/midi-player.css';
import { useEffect, useRef, useState } from 'react';
import { Group, Stack, ActionIcon } from "@mantine/core";
import { Download } from 'lucide-react';

interface AbcPlayerProps {
    abcMusic: string;
    display: boolean
}

export const AbcPlayer: React.FC<AbcPlayerProps> = ({ abcMusic, display }) => {
    const [controler, setControler] = useState<abcjs.SynthObjectController | undefined>(undefined);
    const [visualObj, setVisualObj] = useState<abcjs.TuneObject | undefined>(undefined);
    const paperRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (display) {
            handleInit();
        }
        // TODO - highlight current playing note
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

    const handleInit = async () => {
        {/* called when it is initialize */}
        try {
            console.log('Initializing synth...');
            //get context audio!
            const contextAudio = new (window.AudioContext || (window as any).webkitAudioContext)();

            // create abc representation: "paper" create image and audio, "*" only audio
            const visualObj = abcjs.renderAbc("paper", abcMusic, {
                responsive: "resize",
                add_classes: true, // save classes from abc
            })[0]; // get only first tune

            // TODO - handle multiple tunes

            // create audio
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
        }
    };


    const handleEvent = (ev: any) => {
        // TODO - highlight current playing note
        document.querySelectorAll('.abcjs-note').forEach(note => note.classList.remove('highlighted'));

        if (ev && ev.elements) {
            // Resaltar las notas activas
            ev.elements.forEach((element: Element) => {
                element.classList.add('highlighted');
            });
        }
    };

    const handleBeat = (beatNumber: number, totalBeats: number, beatFraction: number) => {
        // TODO - highlight current playing note
        const currentNotes = document.querySelectorAll(`.abcjs-note`);
        currentNotes.forEach(note => note.classList.remove('highlighted'));

        const highlightedNotes = document.querySelectorAll(`.abcjs-note.abcjs-beat-${beatNumber}`);
        highlightedNotes.forEach(note => note.classList.add('highlighted'));
    };

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
            const svgString = new XMLSerializer().serializeToString(svgElement);
    
            const blob = new Blob([svgString], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);
    
            const a = document.createElement('a');
            a.href = url;
            a.download = 'partitura.svg'; // Nombre del archivo descargado
            a.click();
    
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