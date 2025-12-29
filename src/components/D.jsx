import { useContext } from "react";
import { context } from "./Store";

export default function A(){
    const {count} = useContext(context);
    return(
        <div>
            <h1>D</h1>
            {count}
        </div>
    )
}