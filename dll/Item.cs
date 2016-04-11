using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ServidorPythonEpson
{
    public class Item
    {
        public int Cantidad { get; set; }
        public string Nombre { get; set; }
        public decimal PrecioUnitario { get; set; }
        public decimal Descuento { get; set; }

        public Item(string nombre, int cantidad, decimal precioUnitario, decimal descuento)
        {
            Cantidad = cantidad;
            Nombre = nombre;
            PrecioUnitario = precioUnitario;
            Descuento = descuento;
        }

        public Item(string nombre, int cantidad, decimal precioUnitario)
        {
            Cantidad = cantidad;
            Nombre = nombre;
            PrecioUnitario = precioUnitario;
            Descuento = 0;
        }
    }
}
