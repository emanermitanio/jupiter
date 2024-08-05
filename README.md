 @media print {
            /* Ensure landscape orientation */
            @page {
                size: landscape;
            }

            /* Optionally, hide elements not needed in the print version */
            .no-print {
                display: none;
            }
            .content{
              margin-left: 0 !important;
            }
        }


  <a class="nav-link txt-white ms-3" onclick="window.print();"><i
              class="fa-solid fa-plus me-1"></i>PRINT</a>
