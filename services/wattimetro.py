import cmath
from math import radians, degrees, cos
import re

class Wattimetro:
    """
    Representa um Wattímetro.
    Armazena |V|, |I| e a fase (em radianos) e calcula a Potência Ativa (W).
    """

    def __init__(self, *, modV=None, modI=None, rad=None, gr=None):
        """
        Inicializa o Wattímetro.
        É necessário fornecer 'modV' E 'modI' E ('rad' OU 'gr').
        """
        
        # 1. Validação de entrada
        if (modV is not None and modI is not None) and (rad is not None or gr is not None):
            
            if gr is not None:
                self._rad = radians(gr)
            elif rad is not None:
                self._rad = rad
            
            self._modV = modV
            self._modI = modI
            
        else:
            raise ValueError(
                'Entrada inválida. Forneça "modV" E "modI" E ("rad" OU "gr").'
            )

    def value(self) -> dict:
        """
        Calcula e retorna V, I, Fase (graus) e Potência Ativa (W).
        Potência Ativa (W) = |V| * |I| * cos(Alpha)
        """
        # CORREÇÃO AQUI: Passar o ângulo em radianos para a função cos()
        potencia_ativa = self._modV * self._modI * cos(self._rad)
        
        return {
            'V'     : self._modV ,
            'I'     : self._modI ,
            'Alpha' : degrees(self._rad) ,
            'W'     : potencia_ativa,
        }
    
    # --- 1. Operações Aritméticas entre objetos Wattimetro (Retorna FLOAT) ---
    
    def __add__(self, other):
        """Sobrecarga do operador '+' (obj1 + obj2). Retorna obj1.W + obj2.W."""
        if isinstance(other, Wattimetro):
            return self.value()['W'] + other.value()['W']
        return NotImplemented

    # --- NOVO MÉTODO PARA CORRIGIR O ERRO 'sum()' ---
    def __radd__(self, other):
        """
        Sobrecarga para adição reversa (ex: 0 + Wattimetro).
        Permite que a função sum() funcione, retornando a potência (float) 
        quando o valor inicial (other) é 0.
        """
        if other == 0:
            # Retorna o valor de potência (float) para que a soma continue com floats.
            return self.value()['W']
        # Se 'other' for um float ou int diferente de 0, tenta a adição normal (float + float)
        if isinstance(other, (int, float)):
            return other + self.value()['W']
        return NotImplemented

    def __sub__(self, other):
        """Sobrecarga do operador '-' (obj1 - obj2). Retorna obj1.W - obj2.W."""
        if isinstance(other, Wattimetro):
            return self.value()['W'] - other.value()['W']
        return NotImplemented

    def __mul__(self, other):
        """Sobrecarga do operador '*' (obj1 * obj2). Retorna obj1.W * obj2.W."""
        # Se for entre dois Wattímetros, retorna a multiplicação das potências.
        if isinstance(other, Wattimetro):
            return self.value()['W'] * other.value()['W']
        
        # --- 2. Operação com Escalar: obj1 * escalar ---
        # Se for um escalar, retorna o W * escalar
        if isinstance(other, (int, float)):
            return self.value()['W'] * other
        return NotImplemented

    def __truediv__(self, other):
        """Sobrecarga do operador '/' (obj1 / obj2). Retorna obj1.W / obj2.W."""
        # Se for entre dois Wattímetros, retorna a divisão das potências.
        if isinstance(other, Wattimetro):
            return self.value()['W'] / other.value()['W']
        
        # --- 2. Operação com Escalar: obj1 / escalar ---
        # Se for um escalar, retorna o W / escalar
        if isinstance(other, (int, float)):
            return self.value()['W'] / other
        return NotImplemented
    
    # --- 2. Operações Aritméticas Reversas (Escalar * obj1) ---

    def __rmul__(self, other):
        """Sobrecarga reversa do operador '*' (escalar * obj1)."""
        # Se o outro operando for um número (int ou float), usa a multiplicação normal.
        if isinstance(other, (int, float)):
            return self * other # Chama __mul__ (self.W * other)
        return NotImplemented

    def __rtruediv__(self, other):
        """Sobrecarga reversa do operador '/' (escalar / obj1). Retorna escalar / obj1.W."""
        # Se o outro operando for um número, retorna o escalar dividido pela Potência Ativa (W).
        if isinstance(other, (int, float)):
            return other / self.value()['W']
        return NotImplemented
    
    # --- Métodos de Representação ---

    def __repr__(self):
        return f"Wattimetro(modV={self._modV:.4f}, modI={self._modI:.4f}, gr={degrees(self._rad):.4f})"
    
    def __str__(self):
        graus = degrees(self._rad)
        W = self.value()['W']
        return f"V = {self._modV:.4f}, I = {self._modI:.4f}, \u03B1 = {graus:.4f}° | w = {W:.4f} W"


if __name__ == "__main__":
    
    # Fasores de teste
    # W1: 10 * 2 * cos(60) = 20 * 0.5 = 10.0
    obj1 = Wattimetro(modV=10, modI=2, gr=60)
    
    # W2: 5 * 3 * cos(0) = 15 * 1.0 = 15.0
    obj2 = Wattimetro(modV=5, modI=3, gr=0)
    
    print(f"Objeto 1: {obj1}")
    print(f"Potência W1: {obj1.value()['W']:.1f}")
    print(f"Objeto 2: {obj2}")
    print(f"Potência W2: {obj2.value()['W']:.1f}")
    print("-" * 30)

    # --- 1. Operações entre Wattímetros ---
    
    # Soma (10.0 + 15.0 = 25.0)
    resultado_soma = obj1 + obj2
    print(f"obj1 + obj2 = {resultado_soma}")
    print(f"Tipo: {type(resultado_soma) == float}")

    # Subtração (10.0 - 15.0 = -5.0)
    resultado_sub = obj1 - obj2
    print(f"obj1 - obj2 = {resultado_sub}")
    
    # Multiplicação (10.0 * 15.0 = 150.0)
    resultado_mult = obj1 * obj2
    print(f"obj1 * obj2 = {resultado_mult}")
    
    # Divisão (10.0 / 15.0 = 0.666...)
    resultado_div = obj1 / obj2
    print(f"obj1 / obj2 = {resultado_div}")

    print("-" * 30)

    # --- 2. Produto e Quociente por Escalar ---
    escalar = 2.5
    
    # Escalar * obj1 (2.5 * 10.0 = 25.0)
    resultado_rmul = escalar * obj1
    print(f"{escalar} * obj1 = {resultado_rmul}")
    print(f"Resultado == {escalar * obj1.value()['W']:.1f}: {resultado_rmul == escalar * obj1.value()['W']}")

    # obj1 * Escalar (10.0 * 2.5 = 25.0)
    resultado_mul = obj1 * escalar
    print(f"obj1 * {escalar} = {resultado_mul}")

    # Escalar / obj1 (2.5 / 10.0 = 0.25)
    resultado_rdiv = escalar / obj1
    print(f"{escalar} / obj1 = {resultado_rdiv}")

    # obj1 / Escalar (10.0 / 2.5 = 4.0)
    resultado_div_escalar = obj1 / escalar
    print(f"obj1 / {escalar} = {resultado_div_escalar}")