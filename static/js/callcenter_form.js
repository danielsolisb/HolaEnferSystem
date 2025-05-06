document.addEventListener('DOMContentLoaded', function () {
    // Referencias a Elementos del DOM
    const ciudadSelect = document.getElementById('ciudad-select');
    const zonaSelect = document.getElementById('zona-select');
    const coverageErrorDiv = document.getElementById('coverage-error');
    const calendarPlaceholder = document.getElementById('calendar-placeholder');
    const slotErrorDiv = document.getElementById('slot-error');
    const selectedSlotInfoDiv = document.getElementById('selected-slot-info');
    const selectedDateInput = document.getElementById('selected-date');
    const selectedTimeInput = document.getElementById('selected-time');

    const nurseSelectionArea = document.getElementById('nurse-selection-area');
    const nurseSelect = document.getElementById('nurse-select');
    const nurseErrorDiv = document.getElementById('nurse-error');
    const selectedNurseIdInput = document.getElementById('selected-nurse-id');

    const serviceSelect = document.getElementById('service-select');
    const selectedServiceIdInput = document.getElementById('selected-service-id');
    const serviceRequiresRemovalInput = document.getElementById('service-requires-removal');
    const productSelect = document.getElementById('product-select'); // Asumiendo que quieres manejarlo
    const selectedProductIdInput = document.getElementById('selected-product-id');

    const removalSection = document.getElementById('removal-section');
    const removalDateInput = document.getElementById('removal-date');
    const removalTimeInput = document.getElementById('removal-time');
    const removalErrorDiv = document.getElementById('removal-error');

    const patientCedulaSearchInput = document.getElementById('patient-cedula-search');
    const searchPatientBtn = document.getElementById('search-patient-btn');
    const patientSearchErrorDiv = document.getElementById('patient-search-error');
    const patientDetailsDisplayDiv = document.getElementById('patient-details-display');
    const patientNameDisplaySpan = document.getElementById('patient-name-display');
    const selectedPatientIdInput = document.getElementById('selected-patient-id');

    const createPatientFormArea = document.getElementById('create-patient-form-area');
    const newPatientNombresInput = document.getElementById('new-patient-nombres');
    const newPatientApellidosInput = document.getElementById('new-patient-apellidos');
    const newPatientCedulaInput = document.getElementById('new-patient-cedula'); // Se pre-llena
    const newPatientTelefonoInput = document.getElementById('new-patient-telefono');
    const newPatientEmailInput = document.getElementById('new-patient-email');
    const newPatientCiudadSelect = document.getElementById('new-patient-ciudad'); // Deberías poblar esto también
    const newPatientDireccionTextarea = document.getElementById('new-patient-direccion');
    const newPatientMapaInput = document.getElementById('new-patient-mapa');
    const saveNewPatientBtn = document.getElementById('save-new-patient-btn');
    const cancelNewPatientBtn = document.getElementById('cancel-new-patient-btn');
    const patientCreateErrorDiv = document.getElementById('patient-create-error');

    const tipoUbicacionRadios = document.querySelectorAll('input[name="tipo_ubicacion"]');
    const otraUbicacionDetailsDiv = document.getElementById('otra-ubicacion-details');
    const ubicacionManualTextarea = document.getElementById('ubicacion-manual');
    const mapaManualInput = document.getElementById('mapa-manual');
    const otraUbicacionErrorDiv = document.getElementById('otra-ubicacion-error');


    const doctorNameInput = document.getElementById('doctor-name');
    const appointmentNotesTextarea = document.getElementById('appointment-notes');

    const submitAppointmentBtn = document.getElementById('submit-appointment-btn');
    const submitErrorDiv = document.getElementById('submit-error');
    const submitSuccessDiv = document.getElementById('submit-success');

    // --- >>> INICIO: AÑADIR ESTAS LÍNEAS (NUEVAS REFERENCIAS PARA ESTADO) <<< ---
    const statusSelect = document.getElementById('status-select');
    const selectedStatusIdInput = document.getElementById('selected-status-id'); // Asume que tienes <input type="hidden" id="selected-status-id"> en tu HTML
    const statusErrorDiv = document.getElementById('status-error'); // Asume que tienes <div id="status-error" class="text-danger small mt-1" style="display: none;"></div>
    // --- >>> FIN: AÑADIR ESTAS LÍNEAS <<< ---

    let calendar; // Variable para la instancia de FullCalendar
    let availabilityDataCache = {}; // Cache para la disponibilidad

    // --- Inicialización ---
    initializeCalendar();
    populateNewPatientCiudades(); // Llenar select de ciudad para nuevo paciente

    // --- Helper Functions ---
    function showMessage(element, message, isError = true) {
        element.textContent = message;
        element.className = isError ? 'text-danger small mt-1' : 'text-success small mt-1';
        element.style.display = 'block';
    }

    function hideMessage(element) {
        element.style.display = 'none';
        element.textContent = '';
    }

    function populateSelect(selectElement, options, placeholder) {
        selectElement.innerHTML = `<option value="">${placeholder}</option>`;
        options.forEach(option => {
            selectElement.add(new Option(option.nombre, option.id));
        });
    }

    async function fetchAPI(url, options = {}) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: `Error ${response.status}: ${response.statusText}` }));
                console.error('API Error Data:', errorData);
                throw new Error(errorData.message || `Error ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Fetch API Error:', error);
            throw error; // Re-throw para manejo específico
        }
    }

    function resetDependentFields(level) {
        if (level === 'ciudad') { // Solo si cambia la ciudad, resetea zona y todo lo demás
            zonaSelect.innerHTML = '<option value="">Seleccione Ciudad primero</option>';
            zonaSelect.disabled = true;
            hideMessage(coverageErrorDiv);
            // Y resetea todo lo de 'zona' también
            level = 'zona'; // Hacer que caiga en el siguiente if
        }
    
        if (level === 'zona') { // Si cambia la zona, resetea calendario y slot
            if (calendar) calendar.removeAllEvents();
            selectedSlotInfoDiv.style.display = 'none';
            selectedDateInput.value = '';
            selectedTimeInput.value = '';
            hideMessage(slotErrorDiv);
             // Y resetea todo lo de 'slot'
             // --- >>> INICIO: AÑADIR ESTAS LÍNEAS (RESETEAR ESTADO) <<< ---
             if (statusSelect) {
                statusSelect.addEventListener('change', function() {
                    if (selectedStatusIdInput) selectedStatusIdInput.value = this.value; // Correcto
                    // ...
                    validateAndEnableSubmit(); 
                });
            }// Resetea el dropdown visual
            if (selectedStatusIdInput) selectedStatusIdInput.value = ''; // Resetea el valor guardado
            if (statusErrorDiv) hideMessage(statusErrorDiv); // Oculta errores de estado
            // --- >>> FIN: AÑADIR ESTAS LÍNEAS <<< ---
            level = 'slot'; // Hacer que caiga en el siguiente if
        }
    
        if (level === 'slot') { // Si cambia el slot (o zona o ciudad), resetea enfermeros
            nurseSelectionArea.style.display = 'none';
            nurseSelect.innerHTML = '<option value="">Seleccione Enfermero...</option>';
            selectedNurseIdInput.value = '';
            hideMessage(nurseErrorDiv);
        }
        // Siempre resetear el botón de submit si algo importante cambia
        submitAppointmentBtn.disabled = true;
        hideMessage(submitErrorDiv);
        hideMessage(submitSuccessDiv);
    }


    // --- Event Listeners ---

    ciudadSelect.addEventListener('change', async function () {
        const ciudadId = this.value;
        zonaSelect.disabled = true;
        zonaSelect.innerHTML = '<option value="">Cargando Zonas...</option>';
        resetDependentFields('zona');
        hideMessage(coverageErrorDiv);

        if (ciudadId) {
            try {
                const zonas = await fetchAPI(`${API_URLS.getZonas}?ciudad_id=${ciudadId}`);
                populateSelect(zonaSelect, zonas, 'Seleccione Zona...');
                zonaSelect.disabled = false;
            } catch (error) {
                showMessage(coverageErrorDiv, `Error al cargar zonas: ${error.message}`);
                populateSelect(zonaSelect, [], 'Error al cargar');
            }
        } else {
            populateSelect(zonaSelect, [], 'Seleccione Ciudad primero');
        }
    });

    zonaSelect.addEventListener('change', async function () {
        const zonaId = this.value;
        resetDependentFields('slot'); // Resetea enfermeros y slot seleccionado
        hideMessage(coverageErrorDiv);

        if (zonaId) {
            calendarPlaceholder.innerHTML = 'Cargando disponibilidad...';
            const today = new Date();
            const startDate = today.toISOString().split('T')[0];
            const endDate = new Date(today.setDate(today.getDate() + 6)).toISOString().split('T')[0]; // Próximos 7 días

            try {
                const availability = await fetchAPI(`${API_URLS.availability}?zona_id=${zonaId}&start_date=${startDate}&end_date=${endDate}`);
                availabilityDataCache = availability; // Guardar para uso posterior
                if (Object.keys(availability).length === 0 || Object.values(availability).every(daySlots => Object.keys(daySlots).length === 0)) {
                     showMessage(coverageErrorDiv, 'No hay cobertura o disponibilidad para esta zona en las fechas consultadas.');
                     calendar.removeAllEvents(); // Limpiar calendario
                } else {
                    renderCalendarEvents(availability);
                }
            } catch (error) { // Esto incluye el error 404 de zona no encontrada
                showMessage(coverageErrorDiv, `${error.message}`);
                calendar.removeAllEvents(); // Limpiar calendario
            }
        } else {
            calendar.removeAllEvents();
            calendarPlaceholder.innerHTML = 'Seleccione una zona para ver la disponibilidad.';
        }
    });

    function initializeCalendar() {
        if (calendarPlaceholder) {
            calendar = new FullCalendar.Calendar(calendarPlaceholder, {
                initialView: 'timeGridWeek', // Vista semanal por defecto
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                locale: 'es', // Para español
                slotMinTime: "07:00:00",
                slotMaxTime: "23:00:00", // Muestra hasta esta hora
                height: 'auto', // Intenta ajustar la altura automáticamente
                slotDuration: '01:00:00', // Duración de cada slot en la vista
                allDaySlot: false, // No mostrar slot de "todo el día"
                selectable: true, // Permite seleccionar slots
                selectMirror: true,
                longPressDelay: 0, // para dispositivos móviles
                select: function(info) { // Cuando se selecciona un rango (o se hace click)
                    handleSlotSelection(info);
                },
                eventClick: function(info) { // Si los slots se renderizan como eventos
                    handleSlotSelection(info.event);
                },
                events: [] // Inicialmente vacío, se poblará con API
            });
            calendar.render();
        }
    }

// En callcenter_form.js
    function renderCalendarEvents(availability) {
        calendar.removeAllEvents();
        const events = [];
        console.log("Datos de disponibilidad recibidos por renderCalendarEvents:", JSON.stringify(availability, null, 2)); // DEBUG

        for (const dateStr in availability) {
            if (Object.hasOwnProperty.call(availability, dateStr)) { // Buena práctica
                for (const timeStr in availability[dateStr]) {
                    if (Object.hasOwnProperty.call(availability[dateStr], timeStr)) { // Buena práctica
                        const nursesAvailable = availability[dateStr][timeStr];
                        if (nursesAvailable && nursesAvailable.length > 0) {
                            const startDateTime = `${dateStr}T${timeStr}:00`; // CORREGIDO

                            const [hours, minutes] = timeStr.split(':').map(Number);
                            let endHours = hours + 1;
                            let endMinutes = minutes;
                            let endDateStr = dateStr;

                            if (endHours >= 24) { // Manejo si el slot cruza la medianoche
                                endHours = endHours % 24;
                                let d = new Date(dateStr);
                                d.setDate(d.getDate() + 1);
                                endDateStr = d.toISOString().split('T')[0];
                            }

                            const endTimeStr = `${String(endHours).padStart(2, '0')}:${String(endMinutes).padStart(2, '0')}`;
                            const endDateTime = `${endDateStr}T${endTimeStr}:00`; // CORREGIDO

                            console.log(`Creando evento: ${startDateTime} a ${endDateTime} con ${nursesAvailable.length} enfermeros.`); // DEBUG

                            events.push({
                                title: `Disponible (${nursesAvailable.length} enf.)`,
                                start: startDateTime,
                                end: endDateTime,
                                extendedProps: {
                                    nurses_available_ids: nursesAvailable,
                                    original_time: timeStr // Guardar la hora original del slot
                                }
                            });
                        }
                    }
                }
            }
        }
        if (events.length > 0) {
            calendar.addEventSource(events);
        } else {
            console.log("No se generaron eventos para el calendario."); // DEBUG
            showMessage(coverageErrorDiv, 'No se encontraron slots de disponibilidad para los criterios seleccionados.');
        }
    }

// En callcenter_form.js
// En callcenter_form.js
    async function handleSlotSelection(selectionInfo) {
        const startDate = selectionInfo.start || selectionInfo.startStr; // Para FullCalendar v5/v6
        // Si selectionInfo es un evento, start es un Date. Si es una selección, puede ser startStr.
        let slotDate, slotTime;

        if (startDate instanceof Date) {
            slotDate = startDate.toISOString().split('T')[0];
            slotTime = startDate.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', hour12: false });
        } else { // Asumimos es una cadena como 'YYYY-MM-DDTHH:MM:SS'
            const dateObj = new Date(startDate);
            slotDate = dateObj.toISOString().split('T')[0];
            slotTime = dateObj.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', hour12: false });
        }

        // Si el evento tiene la hora original guardada (por si FullCalendar la ajusta por timezone)
        if (selectionInfo.extendedProps && selectionInfo.extendedProps.original_time) {
            slotTime = selectionInfo.extendedProps.original_time;
        }


        console.log("Slot seleccionado:", slotDate, slotTime); // DEBUG

        selectedDateInput.value = slotDate;
        selectedTimeInput.value = slotTime;
        selectedSlotInfoDiv.textContent = `Slot Seleccionado: ${slotDate} a las ${slotTime}`;
        selectedSlotInfoDiv.style.display = 'block';
        hideMessage(slotErrorDiv);

        const zonaId = zonaSelect.value;
        if (!zonaId) {
            showMessage(slotErrorDiv, "Por favor, seleccione una zona primero.");
            resetDependentFields('slot');
            return;
        }

        nurseSelect.innerHTML = '<option value="">Cargando enfermeros...</option>';
        selectedNurseIdInput.value = '';
        nurseSelectionArea.style.display = 'block';

        try {
            //const nurses = await fetchAPI(`${API_URLS.nursesForSlot}?zona_id=${zonaId}&date=${slotDate}&time=${slotTime}`); // ORIGINAL CON ERROR DE SINTAXIS
            const apiUrlNurses = `${API_URLS.nursesForSlot}?zona_id=${zonaId}&date=${slotDate}&time=${slotTime}`; // CORREGIDO
            console.log("Llamando a API de enfermeros:", apiUrlNurses); //DEBUG
            const nurses = await fetchAPI(apiUrlNurses);

            if (nurses.length > 0) {
                populateSelect(nurseSelect, nurses, 'Seleccione Enfermero...');
                if (nurses.length === 1) {
                    nurseSelect.value = nurses[0].id;
                    selectedNurseIdInput.value = nurses[0].id;
                    console.log("Enfermero único seleccionado automáticamente:", nurses[0].nombre);
                }
                hideMessage(nurseErrorDiv);
            } else {
                showMessage(nurseErrorDiv, 'No hay enfermeros específicos disponibles para este slot. Intente otro.');
                nurseSelectionArea.style.display = 'none';
                // resetDependentFields('slot'); // No resetear todo el slot aquí, solo el área de enfermeros
            }
        } catch (error) {
            showMessage(nurseErrorDiv, `Error al cargar enfermeros: ${error.message}`);
            nurseSelectionArea.style.display = 'none';
            // resetDependentFields('slot');
        }
        validateAndEnableSubmit();
    }

    nurseSelect.addEventListener('change', function() {
        selectedNurseIdInput.value = this.value;
        hideMessage(nurseErrorDiv);
        validateAndEnableSubmit();
    });

    serviceSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        selectedServiceIdInput.value = this.value;
        const requiresRemoval = selectedOption.dataset.requiresRemoval === 'true';
        serviceRequiresRemovalInput.value = requiresRemoval;

        if (requiresRemoval) {
            removalSection.style.display = 'block';
        } else {
            removalSection.style.display = 'none';
            removalDateInput.value = '';
            removalTimeInput.value = '';
            hideMessage(removalErrorDiv);
        }
        validateAndEnableSubmit();
    });

    // Tipo Ubicación
    tipoUbicacionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'otro') {
                otraUbicacionDetailsDiv.style.display = 'block';
            } else {
                otraUbicacionDetailsDiv.style.display = 'none';
                ubicacionManualTextarea.value = '';
                mapaManualInput.value = '';
                hideMessage(otraUbicacionErrorDiv);
            }
             validateAndEnableSubmit();
        });
    });


    searchPatientBtn.addEventListener('click', async function() {
        const cedula = patientCedulaSearchInput.value.trim();
        hideMessage(patientSearchErrorDiv);
        hideMessage(patientCreateErrorDiv);
        patientDetailsDisplayDiv.style.display = 'none';
        createPatientFormArea.style.display = 'none';
        selectedPatientIdInput.value = '';

        if (!cedula) {
            showMessage(patientSearchErrorDiv, 'Por favor, ingrese una cédula.');
            return;
        }

        try {
            // Primera llamada: solo para buscar con la cédula
            const response = await fetchAPI(API_URLS.findCreatePatient, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                },
                body: JSON.stringify({ cedula: cedula })
            });

            if (response.status === 'found') {
                patientNameDisplaySpan.textContent = `${response.nombre} ${response.apellido || ''} (Cédula: ${cedula})`;
                patientDetailsDisplayDiv.style.display = 'block';
                selectedPatientIdInput.value = response.patient_id;
                createPatientFormArea.style.display = 'none'; // Ocultar formulario de creación
                // Podrías pre-llenar campos de ubicación si la cita es a domicilio usando datos de 'response'
            } else if (response.status === 'not_found_enter_details') {
                showMessage(patientSearchErrorDiv, response.message); // "Paciente no encontrado. Por favor, ingrese los detalles..."
                newPatientCedulaInput.value = cedula; // Pre-llenar cédula en el formulario de creación
                // Limpiar otros campos del formulario de nuevo paciente por si acaso
                newPatientNombresInput.value = '';
                newPatientApellidosInput.value = '';
                newPatientTelefonoInput.value = '';
                newPatientEmailInput.value = '';
                if (newPatientCiudadSelect.options.length > 0) newPatientCiudadSelect.value = ''; // Resetear ciudad
                newPatientDireccionTextarea.value = '';
                newPatientMapaInput.value = '';
                createPatientFormArea.style.display = 'block'; // Mostrar formulario para crear
            } else {
                // Otro tipo de error del backend
                showMessage(patientSearchErrorDiv, response.message || response.error || 'Error desconocido al buscar paciente.');
            }
            validateAndEnableSubmit();
        } catch (error) {
            // Error de red o similar
            showMessage(patientSearchErrorDiv, `Error al buscar paciente: ${error.message || 'Error de conexión'}`);
        }
    });

    saveNewPatientBtn.addEventListener('click', async function() {
        hideMessage(patientCreateErrorDiv);
        const patientData = {
            cedula: newPatientCedulaInput.value.trim(), // Ya debería estar pre-llenada
            nombres: newPatientNombresInput.value.trim(),
            apellidos: newPatientApellidosInput.value.trim(),
            telefono: newPatientTelefonoInput.value.trim(),
            email: newPatientEmailInput.value.trim() || null,
            ciudad: newPatientCiudadSelect.value || null,
            direccion: newPatientDireccionTextarea.value.trim() || null,
            ubicacion_mapa: newPatientMapaInput.value.trim() || null,
            // zona: newPatientZonaSelect.value || null, // Si tienes selector de zona para paciente
            // fecha_nacimiento: newPatientFechaNacimientoInput.value || null, // Si tienes este campo
        };
    
        if (!patientData.cedula || !patientData.nombres || !patientData.apellidos || !patientData.telefono /* || !patientData.ciudad || !patientData.direccion */) {
            // Ajusta la validación según los campos realmente obligatorios en tu CustomerProfileForm
            showMessage(patientCreateErrorDiv, 'Cédula, Nombres, Apellidos y Teléfono son requeridos. Ciudad y Dirección también son recomendados.');
            return;
        }
    
        try {
            // Segunda llamada: ahora con todos los datos para crear
            const response = await fetchAPI(API_URLS.findCreatePatient, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                },
                body: JSON.stringify(patientData)
            });
        
            if (response.status === 'created' && response.patient_id) {
                patientNameDisplaySpan.textContent = `${response.nombre} ${response.apellido || ''} (Cédula: ${response.cedula})`;
                patientDetailsDisplayDiv.style.display = 'block';
                selectedPatientIdInput.value = response.patient_id;
                createPatientFormArea.style.display = 'none';
                hideMessage(patientSearchErrorDiv); // Limpiar mensaje de "no encontrado"
                showMessage(patientSearchErrorDiv, 'Paciente creado exitosamente.', false); // Mensaje de éxito temporal
            } else if (response.status === 'validation_error_on_create' && response.errors) {
                let errorMessages = "Error al crear paciente: ";
                for (const field in response.errors) {
                    errorMessages += ` ${field}: ${response.errors[field].join(', ')}.`;
                }
                showMessage(patientCreateErrorDiv, errorMessages);
            } else {
                showMessage(patientCreateErrorDiv, response.message || response.error || 'Error desconocido al crear paciente.');
            }
            validateAndEnableSubmit();
        } catch (error) {
            showMessage(patientCreateErrorDiv, `Error al guardar nuevo paciente: ${error.message || 'Error de conexión'}`);
        }
    });

    cancelNewPatientBtn.addEventListener('click', function() {
        createPatientFormArea.style.display = 'none';
        hideMessage(patientCreateErrorDiv);
        // No resetea el patientCedulaSearchInput para que pueda intentar de nuevo la búsqueda si quiere
    });

    function populateNewPatientCiudades() {
        // Reutilizar la lógica si las ciudades ya están en el DOM principal
        // o hacer una pequeña llamada API si es necesario.
        // Aquí asumo que las ciudades ya están en `ciudadSelect`
        newPatientCiudadSelect.innerHTML = ciudadSelect.innerHTML;
    }

    function validateAndEnableSubmit() {
        // Lógica para habilitar/deshabilitar el botón de submit principal
        // basado en si todos los campos requeridos tienen valor.
        let isValid = true;
        if (!selectedDateInput.value || !selectedTimeInput.value) isValid = false;
        if (!selectedNurseIdInput.value) isValid = false;
        if (!selectedServiceIdInput.value) isValid = false;
        if (!selectedPatientIdInput.value) isValid = false;
        // --- >>> INICIO: AÑADIR ESTA LÍNEA (VALIDACIÓN DE ESTADO) <<< ---
        if (!selectedStatusIdInput.value) isValid = false;
        // --- >>> FIN: AÑADIR ESTA LÍNEA <<< ---

        const tipoUbicacionVal = document.querySelector('input[name="tipo_ubicacion"]:checked').value;
        if (tipoUbicacionVal === 'otro') {
            if (!ubicacionManualTextarea.value.trim() || !mapaManualInput.value.trim()) isValid = false;
        }

        if (serviceRequiresRemovalInput.value === 'true') {
            if (!removalDateInput.value || !removalTimeInput.value) isValid = false;
            // Validar que fecha/hora de retiro sea posterior a aplicación
            if (removalDateInput.value && removalTimeInput.value && selectedDateInput.value && selectedTimeInput.value) {
                const appDateTime = new Date(`${selectedDateInput.value}T${selectedTimeInput.value}`);
                const remDateTime = new Date(`${removalDateInput.value}T${removalTimeInput.value}`);
                if (remDateTime <= appDateTime) {
                    showMessage(removalErrorDiv, "La fecha/hora de retiro debe ser posterior a la aplicación.");
                    isValid = false;
                } else {
                    hideMessage(removalErrorDiv);
                }
            }
        }

        submitAppointmentBtn.disabled = !isValid;
        if(!isValid) {
            hideMessage(submitErrorDiv); // Ocultar si se vuelve inválido
        }
    }

    // Añadir event listeners a campos que afectan la validación para llamar a validateAndEnableSubmit()
    [selectedDateInput, selectedTimeInput, removalDateInput, removalTimeInput, ubicacionManualTextarea, mapaManualInput].forEach(el => {
        if(el) el.addEventListener('change', validateAndEnableSubmit);
    });


    submitAppointmentBtn.addEventListener('click', async function() {
        hideMessage(submitErrorDiv);
        hideMessage(submitSuccessDiv);
        this.disabled = true; // Prevenir doble click
        // --- >>> MODIFICACIÓN AQUÍ <<< ---
        const statusIdFromSelect = statusSelect ? statusSelect.value : null; // Leer directamente del select
        console.log("ID de Estado seleccionado (directo del select):", statusIdFromSelect); // DEBUG
        // --- >>> FIN MODIFICACIÓN <<< ---
        // Recolectar todos los datos
        const payload = {
            patient_id: selectedPatientIdInput.value,
            service_id: selectedServiceIdInput.value,
            nurse_id: selectedNurseIdInput.value,
            application_date: selectedDateInput.value,
            application_time: selectedTimeInput.value,
            tipo_ubicacion: document.querySelector('input[name="tipo_ubicacion"]:checked').value,
            ubicacion_manual: ubicacionManualTextarea.value.trim(),
            status_id: selectedStatusIdInput.value,
            mapa_manual: mapaManualInput.value.trim(),
            producto_id: productSelect.value || null,
            doctor_name: doctorNameInput.value.trim() || null,
            notas: appointmentNotesTextarea.value.trim() || null,
            requires_removal: serviceRequiresRemovalInput.value === 'true',
            removal_date: removalDateInput.value || null,
            removal_time: removalTimeInput.value || null,
        };

        // Validación final (redundante si validateAndEnableSubmit es perfecto, pero buena práctica)
        if (!payload.patient_id || !payload.service_id || !payload.nurse_id ||
            !payload.application_date || !payload.application_time ||
            !payload.status_id // <-- La validación usa el valor del payload
            ) {
            showMessage(submitErrorDiv, "Faltan datos esenciales (Paciente, Servicio, Enfermero, Fecha/Hora, Estado).");
            this.disabled = false;
            return;
        }
        if (payload.tipo_ubicacion === 'otro' && (!payload.ubicacion_manual || !payload.mapa_manual)) {
            showMessage(submitErrorDiv, "Para 'Otra Ubicación', la dirección y el mapa son requeridos.");
             this.disabled = false;
            return;
        }
        if (payload.requires_removal && (!payload.removal_date || !payload.removal_time)) {
            showMessage(submitErrorDiv, "Para servicios con retiro, la fecha y hora de retiro son requeridas.");
             this.disabled = false;
            return;
        }
        if (!payload.patient_id || !payload.service_id || !payload.nurse_id || 
        !payload.application_date || !payload.application_time || 
        !payload.status_id // <-- ¡ASEGÚRATE QUE ESTA VALIDACIÓN ESTÉ PRESENTE Y SEA CORRECTA!
        ) {
        showMessage(submitErrorDiv, "Faltan datos esenciales (Paciente, Servicio, Enfermero, Fecha/Hora, Estado).");
        this.disabled = false;
        return;
    }


        try {
            const response = await fetchAPI(API_URLS.submitAppointment, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                },
                body: JSON.stringify(payload)
            });

            if (response.status === 'success') {
                showMessage(submitSuccessDiv, response.message || 'Cita(s) agendada(s) correctamente.', false);
                // Resetear el formulario o redirigir
                document.getElementById('callcenter-appointment-form').reset(); // Resetear campos nativos
                // Resetear campos y estados personalizados
                resetAllFormStates();
            } else {
                showMessage(submitErrorDiv, response.message || 'Error al agendar la cita.');
            }
        } catch (error) {
            showMessage(submitErrorDiv, `Error de conexión o servidor: ${error.message}`);
        } finally {
            // No re-habilitar inmediatamente si fue exitoso, para que el usuario vea el mensaje.
            // Si falló, sí re-habilitar para que pueda corregir.
            if (submitErrorDiv.style.display === 'block') {
                 this.disabled = false;
            }
        }
    });

    function resetAllFormStates() {
        // Llama a esta función para limpiar el formulario completamente después de un envío exitoso
        ciudadSelect.value = '';
        zonaSelect.innerHTML = '<option value="">Seleccione Ciudad primero</option>';
        zonaSelect.disabled = true;
        hideMessage(coverageErrorDiv);

        if (calendar) {
            calendar.removeAllEvents();
             calendar.gotoDate(new Date());
        }
        selectedSlotInfoDiv.style.display = 'none';
        selectedDateInput.value = '';
        selectedTimeInput.value = '';
        hideMessage(slotErrorDiv);

        nurseSelectionArea.style.display = 'none';
        nurseSelect.innerHTML = '<option value="">Seleccione Enfermero...</option>';
        selectedNurseIdInput.value = '';
        hideMessage(nurseErrorDiv);

        serviceSelect.value = '';
        selectedServiceIdInput.value = '';
        serviceRequiresRemovalInput.value = 'false';
        productSelect.value = '';
        selectedProductIdInput.value = '';


        removalSection.style.display = 'none';
        removalDateInput.value = '';
        removalTimeInput.value = '';
        hideMessage(removalErrorDiv);

        patientCedulaSearchInput.value = '';
        hideMessage(patientSearchErrorDiv);
        patientDetailsDisplayDiv.style.display = 'none';
        patientNameDisplaySpan.textContent = '';
        selectedPatientIdInput.value = '';

        createPatientFormArea.style.display = 'none';
        newPatientNombresInput.value = '';
        newPatientApellidosInput.value = '';
        newPatientCedulaInput.value = '';
        newPatientTelefonoInput.value = '';
        newPatientEmailInput.value = '';
        if (newPatientCiudadSelect.options.length > 0) newPatientCiudadSelect.value = newPatientCiudadSelect.options[0].value;
        newPatientDireccionTextarea.value = '';
        newPatientMapaInput.value = '';
        hideMessage(patientCreateErrorDiv);

        document.querySelector('input[name="tipo_ubicacion"][value="domicilio"]').checked = true;
        otraUbicacionDetailsDiv.style.display = 'none';
        ubicacionManualTextarea.value = '';
        mapaManualInput.value = '';
        hideMessage(otraUbicacionErrorDiv);

        doctorNameInput.value = '';
        appointmentNotesTextarea.value = '';

        submitAppointmentBtn.disabled = true;
        // No ocultar submitSuccessDiv aquí, se oculta al interactuar de nuevo
    }

}); // Fin DOMContentLoaded