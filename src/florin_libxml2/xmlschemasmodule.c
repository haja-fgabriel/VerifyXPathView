#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>


static PyObject *Libxml2SchemasError;


static PyObject*
libxml2_xmlschemas_load_schema(PyObject* self, PyObject* args)
{
    char* str = NULL;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }


    /* Do the C magic */
    printf("Hello from C!\n");

    /* <=> return None */
    return Py_None;
}


static PyMethodDef xmlschemasMethods[] = {
    {"load_schema", libxml2_xmlschemas_load_schema, METH_VARARGS, "Load the schema from the given filepath"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef xmlschemasModule = {
    PyModuleDef_HEAD_INIT,
    "florin_libxml2.xmlschemas",
    "Python interface for the libxml2 xmlschemas module",
    -1,
    xmlschemasMethods
};


PyMODINIT_FUNC
PyInit_xmlschemas(void)
{
    return PyModule_Create(&xmlschemasModule);
}
