# Берет исходный журнал и вырезает лишние символы в поле даты-времени. просто чтобы пока не возиться
# потом копирует каждую строку mult раз просто для того, чтобы нагляднее было время обработки

log_file_path = "C:\\Projects\\IISLogAnalyzer\\input\\access2.log"
mult = 100
with open(log_file_path, 'r') as old, open('C:\\Projects\\IISLogAnalyzer\\input\\access3.log', 'w') as new:
        for line in old:
                pos0 = line.find("[") + 27
                pos = line.find("]")
                line1 = line[:pos0]
                line2 = line[pos:]
                line3 = line1 + line2
                for i in range(mult):
                    new.write(line3)

            