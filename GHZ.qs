namespace GHZ {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Random;
    open Microsoft.Quantum.Preparation;
    open Microsoft.Quantum.Diagnostics;

    operation createGHZState () : Int[] {
        use qubits = Qubit[3];
        H(qubits[0]);
        CNOT(qubits[0], qubits[1]);
        CNOT(qubits[0], qubits[2]);
        let result = MultiM(qubits);
        ResetAll(qubits);
        return result;
    }
}