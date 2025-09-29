import cmath
from math import radians, degrees, cos
import re

class NumFasor:
    """
    Representa um número complexo (fasor).
    Suporta instanciação por: polar (mod, rad ou gr), retangular (a, b) ou STRING (Rect).
    """

    def __init__(self, *, mod=None, rad=None, gr=None, a=None, b=None, Rect=None):
        """
        Inicializa o fasor.
        - Polar: (mod, rad) OU (mod, gr)
        - Retangular: (a, b) OU Rect="a+jb"
        """
        
        # --- 1. Tentativa de Instanciação por String Retangular ---
        if Rect is not None:
            a, b = self._parse_rect_str(Rect)
            self._complex = complex(a, b)
            self._mod, self._rad = cmath.polar(self._complex)

        # --- 2. Instanciação por (mod, fase) ---
        elif mod is not None:
            if rad is not None:
                self._rad = rad
            elif gr is not None:
                self._rad = radians(gr)
            else:
                 raise ValueError("Falta a fase (rad ou gr) para o módulo fornecido.")
            
            self._mod = mod
            self._complex = cmath.rect(mod, self._rad)
            
        # --- 3. Instanciação por (a, b) Retangular ---
        elif a is not None and b is not None:
            self._complex = complex(a, b)
            self._mod, self._rad = cmath.polar(self._complex)
            
        else:
            raise ValueError(
                "Entrada inválida. Forneça (mod e rad/gr) OU (a e b) OU Rect."
            )

    def _parse_rect_str(self, Rect):
        """
        Analisa a string retangular ("a+jb" ou "a+bj") e retorna a parte real (a) e imaginária (b).
        """
        
        # 1. Padronização: Remove espaços, converte para minúsculas.
        s = Rect.strip().lower().replace(' ', '')
        
        # 2. Tratamento para o coeficiente '1' implícito (CORREÇÃO DO ERRO ANTERIOR)
        # Substitui 'j' no início ou após um sinal, se não for seguido por um dígito, por '1j'.
        # Ex: '5+j' -> '5+1j'; 'j3' -> '1j3'
        s = re.sub(r'([+-]|^)(j)(?!\d)', r'\g<1>1j', s)

        # 3. Tratamento para 'j' (isolado) e '-j' (isolado)
        if s == 'j': s = '1j'
        if s == '-j': s = '-1j'

        # 4. Mover a unidade imaginária 'j' para o final do coeficiente (CORREÇÃO DO ERRO ATUAL)
        # Padrão: (sinal opcional) (j) (números e ponto) -> queremos (sinal opcional) (números e ponto) (j)
        # Ex: '5+j3' -> '5+3j'
        s = re.sub(r'([+-]?)j([\d.]+)', r'\1\2j', s)
        
        # O último passo é tratar o 'j' que pode estar no início (ex: 'j3' -> '3j')
        if s.startswith('j') and s != 'j':
            s = s[1:] + 'j' # 'j3' -> '3j'
        
        # 5. Uso do construtor nativo do Python
        try:
            # O construtor `complex()` aceita o formato 'a+bj'
            z = complex(s)
            return z.real, z.imag
        except ValueError:
            raise ValueError(f"Formato de string retangular '{Rect}' inválido após o tratamento interno. String tratada: '{s}'")

    # --- Operações Unárias ---

    def fator_potencia(self):
        """
        Retorna o valor do fator de potência : cos ( \theta ) 
        ⚠︎ Aplicar somente em Potências.
        """
        if self._complex.imag > 0:
            ind_cap = 'ind'
        else:
            ind_cap = 'cap'
        return (cos(self._rad), ind_cap)

    def conjugate(self):
        """
        Calcula o conjugado do fasor (Z*).
        Em polar, inverte o sinal da fase.
        """
        # O módulo permanece o mesmo, a fase é invertida.
        novo_mod = self._mod
        nova_rad = -self._rad
        
        # Retorna uma nova instância de NumFasor
        return NumFasor(mod=novo_mod, rad=nova_rad)

    def __neg__(self):
        """
        Sobrecarga do operador '-' unário (negação, -Z).
        Equivale a adicionar 180 graus (pi radianos) à fase.
        """
        # O módulo permanece o mesmo, a fase é invertida em 180 graus.
        novo_mod = self._mod
        nova_rad = self._rad + cmath.pi
        
        # Retorna uma nova instância de NumFasor
        return NumFasor(mod=novo_mod, rad=nova_rad)

    # --- Propriedades de Leitura (Para acessar os valores internos) ---
    
    @property
    def complex(self):
        """Retorna o fasor na forma complexa (a + bj)."""
        return self._complex

    @property
    def polar_r(self):
        """Retorna o fasor na forma polar (Módulo, Radianos)."""
        return (self._mod, self._rad)

    @property
    def polar_g(self):
        """Retorna o fasor na forma polar (Módulo, Graus)."""
        return (self._mod, degrees(self._rad))


    # --- 2. Implementação das Operações Básicas (Usando sobrecarga de operadores) ---

    def __radd__(self, other):
        """
        Sobrecarga para adição reversa (ex: 0 + NumFasor).
        Se 'other' for 0, usa a complexidade nativa para a soma.
        """
        if other == 0:
            # Retorna o próprio objeto, pois 0 + Z = Z.
            return self
        return NotImplemented # Deixa o Python saber que a operação falhou para outros tipos

    def __add__(self, other):
        """Sobrecarga do operador '+' para adição."""
        if isinstance(other, NumFasor):
            resultado = self._complex + other._complex
            mod, rad = cmath.polar(resultado)
            # Retorna uma nova instância de NumFasor
            return NumFasor(mod=mod, rad=rad)
        return NotImplemented

    def __sub__(self, other):
        """Sobrecarga do operador '-' para subtração."""
        if isinstance(other, NumFasor):
            resultado = self._complex - other._complex
            mod, rad = cmath.polar(resultado)
            return NumFasor(mod=mod, rad=rad)
        return NotImplemented

    def __mul__(self, other):
        """Sobrecarga do operador '*' para multiplicação."""
        if isinstance(other, NumFasor):
            # Operação mais simples em polar: |Z1|*|Z2| ∡ (θ1 + θ2)
            mod = self._mod * other._mod
            rad = self._rad + other._rad
            return NumFasor(mod=mod, rad=rad)
        return NotImplemented
    
    def __truediv__(self, other):
        """Sobrecarga do operador '/' para divisão."""
        if isinstance(other, NumFasor):
            # Operação mais simples em polar: |Z1|/|Z2| ∡ (θ1 - θ2)
            mod = self._mod / other._mod
            rad = self._rad - other._rad
            return NumFasor(mod=mod, rad=rad)
        return NotImplemented
    
    # --- 3. Formato de Retorno para o print() ---

    def rValues(self):
        return

    def __repr__(self):
        """Formato de representação para debug e console."""
        return f"NumFasor(mod={self._mod:.4f}, gr={degrees(self._rad):.4f})"
    
    def __str__(self):
        """Retorna a string formatada para o print() (Polar em Graus)."""
        graus = degrees(self._rad)
        return f"{self._mod:.4f} \u2220 {graus:.4f}°" # \u2220 é o símbolo de ângulo

    def display_polar_r(self):
        """3.1 print(obj_test.polar_r()) => mod ∡ rad (Com formatação SymPy)"""
        return f"Módulo: {self._mod:.4f} ∡ Fase: {self._rad:.4f} rad"

    def __pow__(self, exponente):
        """
        Sobrecarga do operador '**' para potência (z**n).
        Aplica a fórmula de De Moivre para expoentes reais (inteiros ou não, positivos ou negativos).
        """
        if not isinstance(exponente, (int, float)):
             raise TypeError("O expoente deve ser um número real (inteiro ou float).")
        
        # O novo módulo é: |Z|^n
        novo_mod = self._mod ** exponente
        
        # A nova fase é: n * θ
        nova_rad = self._rad * exponente
        
        # Retorna uma nova instância de NumFasor
        return NumFasor(mod=novo_mod, rad=nova_rad)
    
if __name__ == "__main__":
    # 1. Instanciação inicial
    obj_test_g = NumFasor(mod=380, gr=30)
    obj_test_r = NumFasor(mod=10, rad=cmath.pi/4) # 45 graus
    obj_test_rect = NumFasor(a=3, b=4) # |Z| = 5

    print("--- 1. Instanciação e Representação ---")
    print(f"obj_test_g (380V, 30°): {obj_test_g}")
    print(f"obj_test_r (10V, 45°): {obj_test_r}")
    print(f"obj_test_rect (3 + 4j): {obj_test_rect}")

    print("\n--- 3. Acessando Formatos de Saída ---")
    # 3.1 print(obj_test.polar_r()) => mod ∡ rad
    print(f"obj_test_g.display_polar_r(): {obj_test_g.display_polar_r()}")
    print(f"obj_test_g.polar_r (tupla): {obj_test_g.polar_r}") # Acesso à tupla
    print(f"obj_test_g.complex: {obj_test_g.complex}") # Acesso ao complexo

    # 2. Operações Básicas (Usando sobrecarga de operadores)
    print("\n--- 2. Operações Básicas ---")

    fasor_a = NumFasor(mod=10, gr=0)
    fasor_b = NumFasor(mod=5, gr=90) # 5i

    # Adição (a + b) -> (10 + 5i)
    soma = fasor_a + fasor_b
    print(f"Soma: {fasor_a} + {fasor_b} = {soma}")
    # Resultado esperado (aproximadamente): 11.1803 ∡ 26.5651°

    # Subtração (a - b) -> (10 - 5i)
    subtracao = fasor_a - fasor_b
    print(f"Subtração: {fasor_a} - {fasor_b} = {subtracao}")

    # Multiplicação (a * b) -> (10*5) ∡ (0° + 90°)
    multiplicacao = fasor_a * fasor_b
    print(f"Multiplicação: {fasor_a} * {fasor_b} = {multiplicacao}")
    # Resultado esperado: 50.0000 ∡ 90.0000°

    # Divisão (a / b) -> (10/5) ∡ (0° - 90°)
    divisao = fasor_a / fasor_b
    print(f"Divisão: {fasor_a} / {fasor_b} = {divisao}")
    # Resultado esperado: 2.0000 ∡ -90.0000°

    print("\n--- Teste da Operação de Potência (**) ---")

    # Fasor de teste: Z = 2 ∡ 30°
    fasor_z = NumFasor(mod=2, gr=30)
    print(f"Fasor Z: {fasor_z}")

    # Potência Positiva (Z**2)
    # Resultado esperado: 2² ∡ (2 * 30°) = 4 ∡ 60°
    z_quadrado = fasor_z ** 2
    print(f"Z ao quadrado (Z**2): {z_quadrado}") # Deve ser 4.0000 ∡ 60.0000°

    #print("\n")

    # Potência Negativa (Z**-1) - Equivalente a 1/Z (Inverso)
    # Resultado esperado: 2⁻¹ ∡ (-1 * 30°) = 0.5 ∡ -30°
    z_inverso = fasor_z ** -1
    print(f"Z inverso (Z**-1): {z_inverso}") # Deve ser 0.5000 ∡ -30.0000°

    # Raiz Quadrada (Z**0.5)
    # Resultado esperado: sqrt(2) ∡ (30° / 2) = 1.4142 ∡ 15°
    z_raiz = fasor_z ** 0.5
    print(f"Raiz de Z (Z**0.5): {z_raiz}") # Deve ser 1.4142 ∡ 15.0000°

    # ---
    # Exemplo de Uso do Conjugado e Negação
    # ---
    print("\n--- Teste de Conjugado e Negação ---")

    # Fasor de teste: Z = 10 ∡ 45°
    fasor_z = NumFasor(mod=10, gr=45)
    print(f"Fasor Z: {fasor_z}") # 10.0000 ∡ 45.0000°

    # 1. Conjugado (Z*)
    # Resultado esperado: 10 ∡ -45°
    z_conjugado = fasor_z.conjugate()
    print(f"Conjugado Z*: {z_conjugado}") # 10.0000 ∡ -45.0000°

    #print("\n")

    # 2. Negação (-Z)
    # Resultado esperado: 10 ∡ (45° + 180°) = 10 ∡ 225°
    z_negado = -fasor_z 
    print(f"Negação -Z: {z_negado}") # 10.0000 ∡ 225.0000°

    # ---
    # Exemplos de Uso com String Retangular
    # ---
    print("--- Teste de Instanciação com String Retangular ---")

    # 1. Casos completos
    f1 = NumFasor(Rect="5+j3")
    print(f"5+j3: {f1}") # Esperado: 5.8310 ∡ 30.9638°

    f2 = NumFasor(Rect="10 - 5j")
    print(f"10 - 5j: {f2}") # Esperado: 11.1803 ∡ -26.5651°

    # 2. Casos puros (apenas real ou apenas imaginário)
    f3 = NumFasor(Rect="-8")
    print(f"-8 (Real puro): {f3}") # Esperado: 8.0000 ∡ 180.0000°

    f4 = NumFasor(Rect="j3")
    print(f"j3 (Imaginário puro): {f4}") # Esperado: 3.0000 ∡ 90.0000°

    # 3. Coeficiente 1 (implícito)
    f5 = NumFasor(Rect="5-j")
    print(f"5-j: {f5}") # Esperado: 5.0990 ∡ -11.3099°