import { Skeleton, ScrollArea } from "@mantine/core";
import { Scroll } from "lucide-react";

export const Examples: React.FC = () => {
    return (
        <>
       <h1>Ejemplos</h1>
       <ScrollArea style={{ height: "400px", width: "100%" }} type="auto">
       <Skeleton>
              <p style={{height:500}}>Contenido</p>
       </Skeleton>
         </ScrollArea>
       </>
    );
}